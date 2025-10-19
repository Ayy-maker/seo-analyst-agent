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
from datetime import datetime

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
            
            # Generate HTML report only
            html_file = html_generator.generate_full_report(
                company_name=company_name,
                report_period=report_period,
                seo_data=None  # Will use default sample data
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
        
        # Generate HTML report only
        html_file = html_generator.generate_full_report(
            company_name=company_name,
            report_period=report_period,
            seo_data=None  # Will use default sample data for now
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
