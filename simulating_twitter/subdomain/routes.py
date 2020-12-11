from flask import Blueprint, render_template


subdomain = Blueprint('subdomain', __name__)


@subdomain.route('/subdomain/ads')
def subdomain_ads():
    return render_template('subdomain_ads.html')


@subdomain.route('/subdomain/analytics')
def subdomain_analytics():
    return render_template('subdomain_analytics.html')


@subdomain.route('/subdomain/support')
def subdomain_support():
    return render_template('subdomain_support.html')


@subdomain.route('/subdomain/about')
def subdomain_about():
    return render_template('subdomain_about.html')


@subdomain.route('/subdomain/status')
def subdomain_status():
    return render_template('subdomain_status.html')


@subdomain.route('/subdomain/business')
def subdomain_business():
    return render_template('subdomain_business.html')


@subdomain.route('/subdomain/developer')
def subdomain_developer():
    return render_template('subdomain_developer.html')