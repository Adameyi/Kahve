# views.py

from django.shortcuts import render

def handler404(request, exception):
    # Customize the error message based on the exception
    error_message = str(exception) if exception else "Page not found"

    # Render the 404.html template with the error message
    return render(request, 'cafe/404.html', {'error_message': error_message}, status=404)
