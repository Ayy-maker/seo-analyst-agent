"""
MODERN WEB INTERFACE
Easy file upload, report generation, and client management
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import sys
import sqlite3

# Add project to path
sys.path.append(str(Path(__file__).parent.parent))

from database import DatabaseManager
from parsers import CSVParser, XLSXParser, DOCXParser, PDFParser
from agents.analyst import AnalystAgent
from agents.critic import CriticAgent
from agents.reporter.enhanced_html_generator import EnhancedHTMLGenerator
from agents.analyst.competitor_analyzer import CompetitorAnalyzer
from utils.data_normalizer import data_normalizer
from datetime import datetime

# Google API clients for automated data fetching
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / 'integrations'))
    from gsc_api_client import GSCAPIClient
    from ga4_api_client import GA4APIClient
    GOOGLE_APIS_AVAILABLE = True
except ImportError:
    GOOGLE_APIS_AVAILABLE = False
    print("⚠️  Google API clients not available. Service account automation disabled.")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

CORS(app)

# Add basename filter for templates
@app.template_filter('basename')
def basename_filter(path):
    """Get basename of a file path"""
    return os.path.basename(path) if path else ''

# Initialize components
db = DatabaseManager()
html_generator = EnhancedHTMLGenerator()
competitor_analyzer = CompetitorAnalyzer(db)

# Allowed extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'docx', 'doc', 'pdf', 'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ============== AUTOMATION HELPERS ==============

def auto_fetch_google_data(company_name: str, domain: str = None) -> dict:
    """
    Automatically fetch GSC and GA4 data using service account

    Args:
        company_name: Company name for reporting
        domain: Website domain (optional, will try to detect from GSC sites)

    Returns:
        dict with 'gsc_data' and 'ga4_data' keys
    """
    result = {
        'gsc_data': None,
        'ga4_data': None,
        'gsc_error': None,
        'ga4_error': None,
        'gsc_fetched': False,
        'ga4_fetched': False
    }

    if not GOOGLE_APIS_AVAILABLE:
        result['gsc_error'] = "Google API clients not installed"
        result['ga4_error'] = "Google API clients not installed"
        return result

    # Try to fetch GSC data
    try:
        gsc_client = GSCAPIClient()

        if gsc_client.connect():
            print(f"✅ GSC Connected via {gsc_client.auth_method}")

            # List available sites
            sites = gsc_client.list_sites()

            if not sites:
                result['gsc_error'] = "No GSC sites found. Add service account to GSC."
            else:
                # Use first site or try to find matching domain
                target_site = sites[0]
                if domain:
                    for site in sites:
                        if domain in site:
                            target_site = site
                            break

                print(f"📊 Fetching GSC data from: {target_site}")

                # Fetch 30 days of data
                queries = gsc_client.fetch_queries_with_metrics(target_site, days=30)

                if queries:
                    # Convert to format expected by normalizer
                    gsc_parsed = {
                        'source': 'Google Search Console',
                        'site_url': target_site,
                        'record_count': len(queries),
                        'data': queries
                    }
                    result['gsc_data'] = gsc_parsed
                    result['gsc_fetched'] = True
                    print(f"✅ Fetched {len(queries)} GSC queries")
                else:
                    result['gsc_error'] = "No GSC data available for selected site"
        else:
            result['gsc_error'] = "GSC connection failed. Check service account setup."
    except Exception as e:
        result['gsc_error'] = f"GSC error: {str(e)}"
        print(f"❌ GSC Error: {e}")

    # Try to fetch GA4 data
    try:
        ga4_client = GA4APIClient()

        if not ga4_client.property_id:
            result['ga4_error'] = "GA4 Property ID not set"
        elif ga4_client.connect():
            print(f"✅ GA4 Connected via {ga4_client.auth_method}")

            # Fetch 30 days of data
            behavior_data = ga4_client.fetch_user_behavior(days=30)

            if 'error' not in behavior_data:
                # Convert to format expected by normalizer
                ga4_parsed = {
                    'source': 'Google Analytics 4',
                    'property_id': ga4_client.property_id,
                    'record_count': behavior_data.get('total_rows', 0),
                    'data': behavior_data.get('data', [])
                }
                result['ga4_data'] = ga4_parsed
                result['ga4_fetched'] = True
                print(f"✅ Fetched {behavior_data.get('total_rows', 0)} days of GA4 data")
            else:
                result['ga4_error'] = behavior_data.get('error', 'Unknown GA4 error')
        else:
            result['ga4_error'] = "GA4 connection failed. Check service account setup."
    except Exception as e:
        result['ga4_error'] = f"GA4 error: {str(e)}"
        print(f"❌ GA4 Error: {e}")

    return result


# ============== ROUTES ==============

@app.route('/')
def index():
    """Homepage with upload interface"""
    clients = db.get_all_clients()
    return render_template('index.html', clients=clients)


@app.route('/upload-batch', methods=['GET', 'POST'])
def upload_batch():
    """Handle multiple file uploads, auto-sort by brand, generate separate reports"""
    
    if request.method == 'GET':
        return redirect(url_for('index'))
    
    if 'files' not in request.files:
        flash('No files uploaded', 'error')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        flash('No files selected', 'error')
        return redirect(url_for('index'))
    
    report_period = request.form.get('report_period', datetime.now().strftime('%B %Y'))
    
    results = []
    upload_folder = Path(app.config['UPLOAD_FOLDER'])
    upload_folder.mkdir(exist_ok=True)
    
    # Group files by brand name
    brand_files = {}
    all_uploaded_files = []
    
    for file in files:
        if not file or file.filename == '' or not allowed_file(file.filename):
            continue
        
        try:
            # Extract brand name from filename
            company_name = extract_brand_name(file.filename)
            
            # Save file
            filename = secure_filename(file.filename)
            filepath = upload_folder / filename
            file.save(str(filepath))
            
            # Parse file
            ext = filepath.suffix.lower()
            parsers = {
                '.csv': CSVParser(),
                '.xlsx': XLSXParser(),
                '.xls': XLSXParser(),
                '.docx': DOCXParser(),
                '.doc': DOCXParser(),
                '.pdf': PDFParser(),
            }
            
            parser = parsers.get(ext)
            if not parser:
                results.append({
                    'filename': filename,
                    'company': company_name,
                    'status': 'error',
                    'message': 'Unsupported file type'
                })
                continue
            
            parsed_data = parser.parse(str(filepath))
            
            if 'error' in parsed_data:
                results.append({
                    'filename': filename,
                    'company': company_name,
                    'status': 'error',
                    'message': parsed_data['error']
                })
                continue
            
            # Analyze
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                analyst = AnalystAgent(api_key, "config")
                critic = CriticAgent({}, {})
                insights = analyst.analyze(parsed_data)
                validation = critic.validate(insights)
                approved_insights = critic.filter_approved_insights(insights, validation)
            else:
                approved_insights = _create_sample_insights(parsed_data)
            
            # Get or create client
            client = db.get_client(name=company_name)
            if not client:
                client_id = db.create_client(company_name, domain="example.com")
            else:
                client_id = client['id']
            
            # Store report
            health_score = 100 - (len([i for i in approved_insights if i.get('severity') == 'high']) * 8)
            report_id = db.create_report(
                client_id=client_id,
                report_date=datetime.now().date(),
                report_period=report_period,
                insights_count=len(approved_insights),
                health_score=health_score
            )
            db.save_insights(report_id, client_id, approved_insights)

            # Normalize data based on source type
            normalized_data = None
            ga4_metrics = None

            source = parsed_data.get('source', 'Unknown')
            is_semrush = 'semrush' in source.lower() or 'keyword' in parsed_data.get('type', '').lower()

            if source == 'Google Search Console':
                normalized_data = data_normalizer.normalize_gsc_data(parsed_data, company_name)
            elif source == 'Google Analytics 4':
                ga4_metrics = data_normalizer.normalize_ga4_data(parsed_data)
                # If we have GA4 but no GSC, we can't generate full report - use demo GSC with GA4
                normalized_data = None  # Will use demo data, but with GA4 metrics added

            # 🚀 AUTO-FETCH GOOGLE DATA if SEMrush detected but GSC/GA4 missing
            if is_semrush and not (normalized_data and ga4_metrics):
                print(f"\n🚀 Auto-fetching Google data for {company_name}...")

                auto_data = auto_fetch_google_data(company_name)

                # Process GSC data if fetched
                if auto_data['gsc_fetched'] and auto_data['gsc_data']:
                    if not normalized_data:
                        normalized_data = data_normalizer.normalize_gsc_data(auto_data['gsc_data'], company_name)

                # Process GA4 data if fetched
                if auto_data['ga4_fetched'] and auto_data['ga4_data']:
                    if not ga4_metrics:
                        ga4_metrics = data_normalizer.normalize_ga4_data(auto_data['ga4_data'])

            # If we have both GSC and GA4, merge them
            if normalized_data and ga4_metrics:
                normalized_data = data_normalizer.merge_gsc_and_ga4_data(normalized_data, ga4_metrics)
            elif ga4_metrics and not normalized_data:
                # GA4 only - we'll pass ga4_metrics to generator which can handle it
                normalized_data = {'ga4_metrics': ga4_metrics}

            # Generate HTML report with REAL or DEMO data
            html_file = html_generator.generate_full_report(
                company_name=company_name,
                report_period=report_period,
                seo_data=normalized_data  # Uses real data if available, otherwise demo
            )
            
            # Store HTML file path in database
            db.update_report(report_id, file_path=html_file)
            
            results.append({
                'filename': filename,
                'company': company_name,
                'status': 'success',
                'html_file': html_file,
                'insights': len(approved_insights),
                'health_score': health_score,
                'report_id': report_id
            })
            
            # Cleanup
            filepath.unlink()
            
        except Exception as e:
            results.append({
                'filename': file.filename,
                'company': extract_brand_name(file.filename),
                'status': 'error',
                'message': str(e)
            })
    
    # Return beautiful results page (no flash message needed - results page shows everything)
    return render_template('batch_results.html', results=results)


def extract_brand_name(filename):
    """Extract brand/company name from filename"""
    import re
    
    # Remove extension
    name = filename.rsplit('.', 1)[0]
    
    # Try to find "of [brand]" pattern
    of_match = re.search(r'of\s+(.+?)[\s_-]*(?:\d|$)', name, re.IGNORECASE)
    if of_match:
        name = of_match.group(1)
    
    # Clean up
    name = re.sub(r'[\s_-]+', ' ', name)  # Replace separators
    name = re.sub(r'\d{1,2}(?:st|nd|rd|th)?\s+\w+,?\s+\d{4}', '', name, flags=re.IGNORECASE)  # Remove dates
    name = re.sub(r'monthly\s+reports?', '', name, flags=re.IGNORECASE)
    name = re.sub(r'reports?\s+snapshot', '', name, flags=re.IGNORECASE)
    name = re.sub(r'performance\s+on', '', name, flags=re.IGNORECASE)
    name = name.strip()
    
    # Capitalize
    name = ' '.join(word.capitalize() for word in name.split())
    
    return name or 'Unknown Brand'


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle multiple files upload for ONE brand and generate consolidated report"""
    
    if 'files' not in request.files:
        flash('No files uploaded', 'error')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        flash('No files selected', 'error')
        return redirect(url_for('index'))
    
    # Get form data
    company_name = request.form.get('company_name', 'Your Company')
    report_period = request.form.get('report_period', datetime.now().strftime('%B %Y'))
    
    upload_folder = Path(app.config['UPLOAD_FOLDER'])
    upload_folder.mkdir(exist_ok=True)
    
    all_parsed_data = []
    uploaded_files = []
    
    try:
        # Parse all files
        for file in files:
            if not file or file.filename == '' or not allowed_file(file.filename):
                continue
            
            # Save file
            filename = secure_filename(file.filename)
            filepath = upload_folder / filename
            file.save(str(filepath))
            uploaded_files.append(filepath)
            
            # Parse file (skip images for now)
            ext = filepath.suffix.lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                # Images are for visual reference only
                continue
                
            parsers = {
                '.csv': CSVParser(),
                '.xlsx': XLSXParser(),
                '.xls': XLSXParser(),
                '.docx': DOCXParser(),
                '.doc': DOCXParser(),
                '.pdf': PDFParser(),
            }
            
            parser = parsers.get(ext)
            if parser:
                parsed_data = parser.parse(str(filepath))
                if 'error' not in parsed_data:
                    all_parsed_data.append(parsed_data)
        
        if not all_parsed_data:
            flash('No valid data files found', 'error')
            return redirect(url_for('index'))
        
        # Consolidate all parsed data
        consolidated_data = _consolidate_data(all_parsed_data)
        
        # Analyze consolidated data (if API key available)
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            analyst = AnalystAgent(api_key, "config")
            critic = CriticAgent({}, {})
            insights = analyst.analyze(consolidated_data)
            validation = critic.validate(insights)
            approved_insights = critic.filter_approved_insights(insights, validation)
        else:
            # Sample insights
            approved_insights = _create_sample_insights(consolidated_data)
        
        # Get or create client
        client = db.get_client(name=company_name)
        if not client:
            client_id = db.create_client(company_name, domain="example.com")
        else:
            client_id = client['id']
        
        # Store report
        health_score = 100 - (len([i for i in approved_insights if i.get('severity') == 'high']) * 8)
        report_id = db.create_report(
            client_id=client_id,
            report_date=datetime.now().date(),
            report_period=report_period,
            insights_count=len(approved_insights),
            health_score=health_score
        )
        db.save_insights(report_id, client_id, approved_insights)

        # Try to normalize GSC and GA4 data from all uploaded files
        normalized_data = None
        ga4_metrics = None
        has_semrush = False

        # Look for GSC and GA4 data in all parsed files
        for parsed in all_parsed_data:
            source = parsed.get('source', 'Unknown')

            if source == 'Google Search Console' and not normalized_data:
                normalized_data = data_normalizer.normalize_gsc_data(parsed, company_name)
            elif source == 'Google Analytics 4' and not ga4_metrics:
                ga4_metrics = data_normalizer.normalize_ga4_data(parsed)
            elif 'semrush' in source.lower() or 'keyword' in parsed.get('type', '').lower():
                has_semrush = True

        # 🚀 AUTO-FETCH GOOGLE DATA if SEMrush detected but GSC/GA4 missing
        if has_semrush and not (normalized_data and ga4_metrics):
            print(f"\n🚀 Auto-fetching Google data for {company_name}...")
            flash('🚀 Automatically fetching Google Search Console and Analytics data...', 'info')

            auto_data = auto_fetch_google_data(company_name)

            # Process GSC data if fetched
            if auto_data['gsc_fetched'] and auto_data['gsc_data']:
                if not normalized_data:
                    normalized_data = data_normalizer.normalize_gsc_data(auto_data['gsc_data'], company_name)
                    flash('✅ Google Search Console data fetched automatically!', 'success')
            elif auto_data['gsc_error']:
                flash(f"⚠️ GSC auto-fetch: {auto_data['gsc_error']}", 'warning')

            # Process GA4 data if fetched
            if auto_data['ga4_fetched'] and auto_data['ga4_data']:
                if not ga4_metrics:
                    ga4_metrics = data_normalizer.normalize_ga4_data(auto_data['ga4_data'])
                    flash('✅ Google Analytics 4 data fetched automatically!', 'success')
            elif auto_data['ga4_error']:
                flash(f"⚠️ GA4 auto-fetch: {auto_data['ga4_error']}", 'warning')

        # If we have both GSC and GA4, merge them
        if normalized_data and ga4_metrics:
            normalized_data = data_normalizer.merge_gsc_and_ga4_data(normalized_data, ga4_metrics)
        elif ga4_metrics and not normalized_data:
            # GA4 only - use demo GSC data but include GA4 metrics
            normalized_data = {'ga4_metrics': ga4_metrics}

        # Generate HTML report with REAL or DEMO data
        html_file = html_generator.generate_full_report(
            company_name=company_name,
            report_period=report_period,
            seo_data=normalized_data  # Uses real data if available, otherwise demo
        )
        
        # Store HTML file path in database
        db.update_report(report_id, file_path=html_file)
        
        flash(f'Report generated successfully from {len(all_parsed_data)} files!', 'success')
        return redirect(url_for('view_report', report_id=report_id))
        
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        # Cleanup uploaded files
        for filepath in uploaded_files:
            if filepath.exists():
                filepath.unlink()


@app.route('/dashboard')
def dashboard():
    """Multi-client dashboard with real statistics"""
    try:
        clients = db.get_all_clients()
        
        # Calculate real statistics
        total_reports = 0
        total_health_score = 0
        health_count = 0
        
        # Enhance client data with stats
        enhanced_clients = []
        
        if clients:
            for client in clients:
                try:
                    reports = db.get_reports(client['id'])
                    client_reports = len(reports) if reports else 0
                    total_reports += client_reports
                    
                    # Get latest health score
                    latest_health = 0
                    if reports:
                        latest_health = reports[0].get('health_score', 0)
                        total_health_score += latest_health
                        health_count += 1
                    
                    # Add stats to client
                    client_with_stats = dict(client)
                    client_with_stats['report_count'] = client_reports
                    client_with_stats['latest_health'] = latest_health
                    enhanced_clients.append(client_with_stats)
                    
                except Exception as e:
                    print(f"Error getting reports for client {client['id']}: {e}")
                    enhanced_clients.append(dict(client))
        
        # Calculate average health score
        avg_health_score = int(total_health_score / health_count) if health_count > 0 else 0
        
        return render_template('dashboard.html', 
                             clients=enhanced_clients, 
                             total_reports=total_reports,
                             avg_health_score=avg_health_score)
    except Exception as e:
        print(f"Dashboard error: {e}")
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/client/<int:client_id>')
def client_detail(client_id):
    """Client detail page"""
    client = db.get_client(client_id=client_id)
    if not client:
        flash('Client not found', 'error')
        return redirect(url_for('dashboard'))
    
    reports = db.get_reports(client_id, limit=10)
    stats = db.get_client_stats(client_id)
    
    return render_template('client.html', client=client, reports=reports, stats=stats)


@app.route('/reports')
def view_reports():
    """View all reports dashboard"""
    db_path = Path(__file__).parent.parent / 'database' / 'seo_data.db'
    
    # Get all reports with client info
    query = """
        SELECT 
            r.id,
            r.client_id,
            r.report_period,
            r.health_score,
            r.created_at,
            c.name as client_name,
            (SELECT COUNT(*) FROM insights WHERE report_id = r.id) as insight_count
        FROM reports r
        JOIN clients c ON r.client_id = c.id
        ORDER BY r.created_at DESC
    """
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    reports_data = cursor.fetchall()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM reports")
    total_reports = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM clients")
    total_clients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM insights")
    total_insights = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(health_score) FROM reports")
    avg_health_score = cursor.fetchone()[0] or 0
    
    conn.close()
    
    # Format reports
    reports = []
    for row in reports_data:
        try:
            created_dt = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S')
            created_formatted = created_dt.strftime('%b %d, %Y at %I:%M %p')
        except:
            created_formatted = row['created_at']
        
        reports.append({
            'id': row['id'],
            'client_id': row['client_id'],
            'client_name': row['client_name'],
            'report_period': row['report_period'],
            'health_score': row['health_score'],
            'insight_count': row['insight_count'],
            'created_at': row['created_at'],
            'created_at_formatted': created_formatted
        })
    
    return render_template('all_reports.html',
                         reports=reports,
                         total_reports=total_reports,
                         total_clients=total_clients,
                         total_insights=total_insights,
                         avg_health_score=avg_health_score)

@app.route('/report/<int:report_id>')
def view_report(report_id):
    """View report with preview and download options"""
    try:
        # Get report info from database
        reports = db.get_reports(client_id=None, limit=100)  # Get all reports
        report = next((r for r in reports if r['id'] == report_id), None)
        
        if not report:
            flash('Report not found', 'error')
            return redirect(url_for('index'))
        
        # Convert report dict to mutable dict and handle date formatting
        report = dict(report)
        if report.get('created_at'):
            # If it's a string, convert to datetime
            if isinstance(report['created_at'], str):
                try:
                    from dateutil import parser
                    report['created_at'] = parser.parse(report['created_at'])
                except:
                    # If parsing fails, format the string directly
                    report['created_at_formatted'] = report['created_at']
            # Format datetime object
            if hasattr(report.get('created_at'), 'strftime'):
                report['created_at_formatted'] = report['created_at'].strftime('%B %d, %Y at %I:%M %p')
        else:
            report['created_at_formatted'] = 'Recently'
        
        # Get client info
        client = db.get_client(client_id=report['client_id'])
        
        # Get insights
        insights = db.get_insights(report_id, report['client_id'])
        
        # Get HTML path from report database record
        html_path = report.get('file_path', '')
        file_exists = False
        
        # Check if file exists
        if html_path:
            file_path = Path(html_path)
            
            # If path is relative, make it absolute
            if not file_path.is_absolute():
                project_root = Path(__file__).parent.parent
                file_path = project_root / html_path
            
            file_exists = file_path.exists()
            
            if not file_exists:
                flash('Report file not found. Please regenerate the report.', 'warning')
        
        return render_template('report_preview.html', 
                             report=report,
                             client=client,
                             insights=insights,
                             file_exists=file_exists)
    except Exception as e:
        flash(f'Error loading report: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/report/<int:report_id>/download')
def download_report(report_id):
    """Download HTML report by report ID"""
    try:
        # Get report from database
        reports = db.get_reports(client_id=None, limit=100)
        report = next((r for r in reports if r['id'] == report_id), None)
        
        if not report:
            flash('Report not found', 'error')
            return redirect(url_for('index'))
        
        # Get HTML file path
        html_path = report.get('file_path', '')
        if not html_path:
            flash('Report file path not found. Please regenerate the report.', 'error')
            return redirect(url_for('index'))
        
        # Convert to absolute path if needed
        file_path = Path(html_path)
        if not file_path.is_absolute():
            project_root = Path(__file__).parent.parent
            file_path = project_root / html_path
        
        if not file_path.exists():
            flash(f'Report file not found at: {file_path}. Please regenerate the report.', 'error')
            return redirect(url_for('index'))
        
        # Get the client name for a better filename
        client = db.get_client(client_id=report['client_id'])
        client_name = client['name'].replace(' ', '-').lower() if client else 'client'
        download_filename = f"seo-report-{client_name}-{report_id}.html"
        
        return send_file(
            str(file_path), 
            as_attachment=True, 
            download_name=download_filename,
            mimetype='text/html'
        )
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<path:filepath>')
def download_file(filepath):
    """Download generated report files by path"""
    try:
        # filepath is already an absolute path from the template
        file_path = Path(filepath)
        
        # Only convert if it's actually relative
        if not file_path.is_absolute():
            project_root = Path(__file__).parent.parent
            file_path = project_root / filepath
        
        if file_path.exists():
            # Get filename for download
            filename = file_path.name
            return send_file(str(file_path), as_attachment=True, download_name=filename, mimetype='text/html')
        else:
            flash('File not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/report/<int:report_id>/preview')
def preview_report(report_id):
    """Preview HTML report by report ID"""
    try:
        # Get report from database
        reports = db.get_reports(client_id=None, limit=100)
        report = next((r for r in reports if r['id'] == report_id), None)
        
        if not report:
            flash('Report not found', 'error')
            return redirect(url_for('index'))
        
        # Get HTML file path
        html_path = report.get('file_path', '')
        if not html_path:
            flash('Report file path not found', 'error')
            return redirect(url_for('index'))
        
        # Convert to absolute path if needed
        file_path = Path(html_path)
        if not file_path.is_absolute():
            project_root = Path(__file__).parent.parent
            file_path = project_root / html_path
        
        if file_path.exists() and file_path.suffix == '.html':
            return send_file(str(file_path), mimetype='text/html')
        else:
            flash(f'Report file not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error previewing report: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/preview/<path:filepath>')
def preview_file(filepath):
    """Preview HTML report in browser (legacy route)"""
    try:
        # This route is for backward compatibility
        # Try to find the report by file path
        file_path = Path(filepath)
        if not file_path.is_absolute():
            project_root = Path(__file__).parent.parent
            file_path = project_root / filepath
        
        if file_path.exists() and file_path.suffix == '.html':
            return send_file(str(file_path), mimetype='text/html')
        else:
            flash(f'File not found', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error previewing file: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/competitor-analysis', methods=['GET', 'POST'])
def competitor_analysis():
    """Competitor analysis page - fully functional"""
    clients = db.get_all_clients()
    
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        competitor_domain = request.form.get('competitor_domain')
        competitor_name = request.form.get('competitor_name', '')
        
        if not client_id or not competitor_domain:
            flash('Please provide all required information', 'error')
            return redirect(url_for('competitor_analysis'))
        
        try:
            # Add competitor to database
            competitor_id = competitor_analyzer.add_competitor(
                int(client_id), 
                competitor_domain, 
                competitor_name or competitor_domain
            )
            flash(f'✅ Competitor "{competitor_name or competitor_domain}" added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding competitor: {str(e)}', 'error')
        
        return redirect(url_for('competitor_analysis'))
    
    # Get all competitors with client info
    all_competitors = []
    for client in clients:
        try:
            client_competitors = competitor_analyzer.get_competitors(client['id'])
            for comp in client_competitors:
                comp['client_name'] = client['name']
                all_competitors.append(comp)
        except Exception as e:
            print(f"Error getting competitors for client {client['id']}: {e}")
    
    return render_template('competitor_analysis.html', 
                          clients=clients, 
                          competitors=all_competitors)


@app.route('/api/clients')
def api_clients():
    """API: Get all clients"""
    clients = db.get_all_clients()
    return jsonify(clients)


@app.route('/api/client/<int:client_id>/stats')
def api_client_stats(client_id):
    """API: Get client stats"""
    stats = db.get_client_stats(client_id)
    return jsonify(stats)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings page for API configuration"""
    if request.method == 'POST':
        # Update GA4 Property ID
        property_id = request.form.get('ga4_property_id', '').strip()

        if property_id:
            try:
                from integrations.ga4_api_client import ga4_api_client
                ga4_api_client.set_property_id(property_id)
                flash('✅ GA4 Property ID saved successfully!', 'success')
            except Exception as e:
                flash(f'❌ Error saving Property ID: {str(e)}', 'error')
        else:
            flash('⚠️ Please provide a GA4 Property ID', 'warning')

        return redirect(url_for('settings'))

    # GET: Show current settings
    try:
        from integrations.gsc_api_client import GSCAPIClient
        from integrations.ga4_api_client import GA4APIClient
        from pathlib import Path

        # Check service account status
        sa_path = Path(__file__).parent.parent / 'config' / 'credentials' / 'service_account.json'
        service_account_exists = sa_path.exists()

        # Check GSC connection
        gsc_status = "Not configured"
        gsc_sites = []
        if service_account_exists:
            try:
                gsc_client = GSCAPIClient()
                if gsc_client.connect():
                    gsc_status = f"Connected ({gsc_client.auth_method})"
                    gsc_sites = gsc_client.list_sites()
            except:
                gsc_status = "Error connecting"

        # Check GA4 connection
        ga4_status = "Not configured"
        ga4_property = None
        if service_account_exists:
            try:
                ga4_client = GA4APIClient()
                ga4_property = ga4_client.property_id
                if ga4_client.connect():
                    ga4_status = f"Connected ({ga4_client.auth_method})"
                elif not ga4_property:
                    ga4_status = "Property ID not set"
            except:
                ga4_status = "Error connecting"

        return render_template('settings.html',
                             service_account_exists=service_account_exists,
                             gsc_status=gsc_status,
                             gsc_sites=gsc_sites,
                             ga4_status=ga4_status,
                             ga4_property=ga4_property)
    except Exception as e:
        flash(f'Error loading settings: {str(e)}', 'error')
        return redirect(url_for('index'))


def _create_sample_insights(parsed_data):
    """Create sample insights when no API key"""
    return [
        {
            'module': 'keywords',
            'type': 'opportunity',
            'severity': 'high',
            'insight': 'High-priority keyword opportunities identified in your data.',
            'metric_value': 85
        },
        {
            'module': 'technical',
            'type': 'issue',
            'severity': 'high',
            'insight': 'Technical SEO issues requiring immediate attention.',
            'metric_value': 23
        },
        {
            'module': 'content',
            'type': 'opportunity',
            'severity': 'medium',
            'insight': 'Content optimization opportunities identified.',
            'metric_value': 78
        },
    ]


def _consolidate_data(parsed_data_list):
    """Consolidate data from multiple files into one dataset"""
    consolidated = {
        'keywords': [],
        'technical': [],
        'onpage': [],
        'backlinks': [],
        'traffic': []
    }
    
    for data in parsed_data_list:
        for key in consolidated.keys():
            if key in data and isinstance(data[key], list):
                consolidated[key].extend(data[key])
    
    return consolidated


if __name__ == '__main__':
    app.run(debug=True, port=5000)


@app.route('/competitor/<int:competitor_id>/analyze')
def analyze_competitor(competitor_id):
    """Generate competitor analysis report"""
    try:
        # Get competitor info
        with db.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM competitors WHERE id = ?", (competitor_id,))
            competitor = cursor.fetchone()
            
        if not competitor:
            flash('Competitor not found', 'error')
            return redirect(url_for('competitor_analysis'))
        
        competitor_dict = dict(competitor)
        client_id = competitor_dict['client_id']
        
        # Generate analysis report
        report = competitor_analyzer.generate_competitive_report(client_id)
        
        # Get client info
        client = db.get_client(client_id=client_id)
        
        return render_template('competitor_report.html', 
                             competitor=competitor_dict,
                             client=client,
                             report=report)
    except Exception as e:
        flash(f'Error analyzing competitor: {str(e)}', 'error')
        return redirect(url_for('competitor_analysis'))
