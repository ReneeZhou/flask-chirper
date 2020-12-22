from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from simulating_twitter import db, bcrypt
from simulating_twitter.models import User
from simulating_twitter.user_settings.forms import UpdateProfileForm, UpdateAccountForm, \
    UpdatePasswordForm, ConfirmPasswordForm, UpdateScreenNameForm
from simulating_twitter.user_settings.utils import save_image



user_settings = Blueprint('user_settings', __name__)

@user_settings.route('/settings')
def settings():
    if current_user.is_authenticated:
        return redirect(url_for('user_settings.settings_account'))
    else:
        return redirect(url_for('user_settings.settings_account_personalization'))


@user_settings.route('/settings/account/personalization')
def settings_account_personalization():
    return render_template('settings_account_personalization.html')


@user_settings.route('/settings/password', methods = ['GET', 'POST'])
def settings_password():
    form = UpdatePasswordForm()

    if form.validate_on_submit():
        # check if password is the same
        if bcrypt.check_password_hash(current_user.password, form.new_password.data):
            flash('New password cannot be the same as your existing password.')
        elif bcrypt.check_password_hash(current_user.password, form.current_password.data):
            current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            db.session.commit()
            return redirect(url_for('user_settings.settings_account'))
        else:
            flash('The password you entered was incorrect.')

    return render_template('settings_password.html', form = form)


@user_settings.route('/settings/profile', methods = ['GET', 'POST'])
@login_required
def settings_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.background_image.data: 
            current_user.background_image  = save_image(form.background_image.data)

        if form.profile_image.data:
            current_user.profile_image = save_image(form.profile_image.data)

        current_user.name = form.name.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.profile', handle = current_user.handle))
        # POST/GET redirect pattern
        # browser telling you're about to run another POST when you reload your page
        # so us redirecting causing the browser to send a GET, and we won't get that pop up msg from browser
    
    # populate the form fields with existing user data
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.website.data = current_user.website

    if current_user.background_image == '':
        background_image = ''
    elif current_user.background_image:
        background_image = url_for('static', filename = 'img/background_pics/' + current_user.background_image)
    return render_template('settings_profile.html', form = form, background_image = background_image)


# @user_settings.route('/settings/screen_name', methods = ['GET', 'POST'])
# @login_required
# def settings_screenName():
#     form = UpdateAccountForm()

#     if request.method == 'GET':
#         form.handle.data = current_user.handle
#         form.email.data = current_user.email

#     elif form.validate_on_submit():
#         if form.handle.data != current_user.handle or form.email.data != current_user.email: 
#             current_user.handle = form.handle.data
#             current_user.email = form.email.data
#             db.session.commit()
#             flash('Your account has been updated!', 'success')    
#         # needs fixing, it flashes when return to this page
#         return redirect(url_for('user_settings.settings_account'))

#     return render_template('settings_ScreenName.html', form = form)
@user_settings.route('/settings/screen_name', methods = ['GET', 'POST'])
@login_required
def settings_screenName():
    form = UpdateScreenNameForm()

    if request.method == 'GET':
        form.screen_name.data = current_user.handle

    if request.method == 'POST':
        if form.screen_name.data == current_user.handle:
            return redirect(url_for('user_settings.settings_yourChirperData_account'))
        elif form.validate_on_submit():
            current_user.handle = form.screen_name.data
            db.session.commit()
            return redirect(url_for('user_settings.settings_yourChirperData_account'))


    return render_template('settings_ScreenName.html', form = form)


@user_settings.route('/settings/account')
@login_required
def settings_account():
    return render_template('settings_account.html')


@user_settings.route('/settings/security_and_account_access')
@login_required
def settings_securityAndAccountAccess():
    return render_template('settings_securityAndAccountAccess.html')


@user_settings.route('/settings/privacy_and_safety')
@login_required
def settings_privacyAndSafety():
    return render_template('settings_privacyAndSafety.html')


@user_settings.route('/settings/notifications')
@login_required
def settings_notifications():
    return render_template('settings_notifications.html')


@user_settings.route('/settings/accessibility_display_and_languages')
@login_required
def settings_accessibilityDisplayAndLanguages():
    return render_template('settings_accessibilityDisplayAndLanguages.html')


@user_settings.route('/settings/about')
def settings_about():
    return render_template('settings_about.html')


@user_settings.route('/settings/your_chirper_data', methods = ['GET', 'POST'])
def settings_yourChirperData():
    if current_user.is_authenticated:
        form = ConfirmPasswordForm()

        if 'auth_timestamp' not in session:
            if form.validate_on_submit():
                if bcrypt.check_password_hash(current_user.password, form.password.data):
                    session['auth_timestamp'] = datetime.utcnow()
                    return render_template('settings_yourChirperData.html')
                else:
                    flash('The password you entered was incorrect.')

        else:
            if (datetime.utcnow() - session.get('auth_timestamp')).seconds < 300:
                return render_template('settings_yourChirperData.html')

            else:
                session.pop('auth_timestamp')
                return redirect(url_for('user_settings.settings_yourChirperData'))

        return render_template('settings_yourChirperData_auth.html', form = form)
    
    else:
        return render_template('settings_yourChirperData.html')


@user_settings.route('/settings/your_chirper_data/account', methods = ['GET', 'POST'])
def settings_yourChirperData_account():
    if current_user.is_authenticated:
        form = ConfirmPasswordForm()

        if 'auth_timestamp' not in session:
            if form.validate_on_submit():
                if bcrypt.check_password_hash(current_user.password, form.password.data):
                    session['auth_timestamp'] = datetime.utcnow()
                    return render_template('settings_yourChirperData_account.html')
                else:
                    flash('The password you entered was incorrect.')
        else:
            if (datetime.utcnow() - session.get('auth_timestamp')).seconds < 300:
                return render_template('settings_yourChirperData_account.html')
            else: 
                session.pop('auth_timestamp')
                return redirect(url_for('user_settings.settings_yourChirperData_account'))

        
        return render_template('settings_yourChirperData_auth.html', form = form)
    
    else:
        return render_template('settings_yourChirperData_account.html')


@user_settings.route('/settings/phone')
@login_required
def settings_phone():
    return render_template('settings_phone.html')


@user_settings.route('/settings/email')
@login_required
def settings_email():
    return render_template('settings_email.html')


@user_settings.route('/settings/audience_and_tagging')
@login_required
def settings_audienceAndTagging():
    return render_template('settings_audienceAndTagging.html')


@user_settings.route('/settings/country')
@login_required
def settings_country():
    return render_template('settings_country.html')


@user_settings.route('/settings/languages')
@login_required
def settings_languages():
    return render_template('settings_languages.html')


@user_settings.route('/settings/your_chirp_data/gender')
@login_required
def settings_yourChirpData_gender():
    return render_template('settings_yourChirpData_gender.html')


@user_settings.route('/settings/your_chirp_data/age')
@login_required
def settings_yourChirpData_age():
    return render_template('settings_yourChirpData_age.html')


@user_settings.route('/settings/trends')
@login_required
def settings_trends():
    return render_template('settings_trends.html')


@user_settings.route('/settings/content_preferences')
@login_required
def settings_contentPreferences():
    return render_template('settings_contentPreferences.html')


@user_settings.route('/settings/apps_and_sessions')
@login_required
def settings_appsAndSessions():
    return render_template('settings_appsAndSessions.html')