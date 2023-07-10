from django.urls import resolve

def active_directory(request):
    active_directory = None

    current_url = resolve(request.path_info).view_name
    if current_url == 'home':
        active_directory = 'Home'
    elif current_url == 'Features':
        active_directory = 'Features'
    elif current_url == 'Gallery':
        active_directory = 'Gallery'
    elif current_url == 'FAQ':
        active_directory = 'FAQ'
    elif current_url == 'AboutUs':
        active_directory = 'About Us'
    elif current_url == 'ContactUs':
        active_directory = 'Contact Us'
    elif current_url == 'dashboard':
        active_directory = 'Feians'
    elif current_url == 'login':
        active_directory = 'Feians'
    

    return {'active_directory': active_directory}