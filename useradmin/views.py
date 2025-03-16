from django.shortcuts import render
from cargo_app.models import Shipment, Category, CorporateUser
from users.models import User

def index(request):
    # First check if user is logged in
    if 'userid' not in request.COOKIES:
        return render(request, "home/home.html", {
            'firms': CorporateUser.objects.all(),
            'message': 'Invalid operation. Please log in first.',
            'messagetype': 2
        })
    
    # Get the user object safely using get() instead of filter()[0]
    try:
        user = User.objects.get(id=int(request.COOKIES['userid']))
        
        # Then check if user is admin
        if not user.isAdmin:
            return render(request, "home/home.html", {
                'firms': CorporateUser.objects.all(),
                'userid': request.COOKIES['userid'],
                'message': 'Invalid operation. Admin privileges required.',
                'messagetype': 2
            })
        
        # If code reaches here, user is logged in and is admin
        return render(request, 'adminpanel/index.html', {
            'userid': request.COOKIES['userid'],
            'shipmentList': list(Shipment.objects.all()),
            'userList': list(User.objects.all())
        })
    
    except User.DoesNotExist:
        # Handle case where cookie contains invalid user ID
        response = render(request, "home/home.html", {
            'firms': CorporateUser.objects.all(),
            'message': 'Invalid user session. Please log in again.',
            'messagetype': 2
        })
        # Clear the invalid cookie
        response.delete_cookie('userid')
        return response