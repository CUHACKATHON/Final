from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
=======
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import json
import uuid
from datetime import date
from .models import *
from .forms import LoginForm, AppointmentForm, UserRegistrationForm, CounselorRegistrationForm
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .utils.chatbot_logic import get_chatbot_response, analyze_sentiment, extract_keywords


@csrf_exempt
def login_view(request):
    """User login for all roles - supports both form and token-based authentication"""
    if request.user.is_authenticated:
        if request.user.role == 'admin' or request.user.role == 'counselor':
            return redirect('core:dashboard')
        else:
            return redirect('core:index')
    
    # Handle AJAX/JSON requests for token-based authentication
    # Check Content-Type header (may include charset)
    content_type = request.headers.get('Content-Type', '').lower()
    if request.method == 'POST' and ('application/json' in content_type or request.content_type == 'application/json'):
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            
            if not username or not password:
                return JsonResponse(
                    {'error': 'Username and password are required'},
                    status=400
                )
            
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is None:
                return JsonResponse(
                    {'error': 'Invalid username or password'},
                    status=401
                )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            # Also create session for backward compatibility
            login(request, user)
            
            # Get user info
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_verified': user.is_verified if hasattr(user, 'is_verified') else False,
            }
            
            return JsonResponse({
                'success': True,
                'access': access_token,
                'refresh': refresh_token,
                'user': user_data,
                'redirect': get_redirect_url(user)
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    # Handle traditional form submission (backward compatibility)
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Generate JWT tokens for API access
            try:
                refresh = RefreshToken.for_user(user)
                request.session['access_token'] = str(refresh.access_token)
                request.session['refresh_token'] = str(refresh)
            except Exception:
                pass  # If JWT fails, continue with session auth
            
            messages.success(request, f'Welcome back, {user.username}!')
            redirect_url = get_redirect_url(user)
            return redirect(redirect_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})


def get_redirect_url(user):
    """Helper function to determine redirect URL based on user role"""
    if user.role == 'admin' or (user.role == 'counselor' and user.is_verified):
        return 'core:dashboard'
    elif user.role == 'counselor' and not user.is_verified:
        return 'core:index'
    else:
        return 'core:index'


def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('core:index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def register_counselor_view(request):
    """Counselor registration (pending admin verification)"""
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        form = CounselorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                f'Counselor account created! Your account is pending admin verification. '
                f'You will be notified once verified. Username: {user.username}'
            )
            return redirect('core:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CounselorRegistrationForm()
    
    return render(request, 'registration/register_counselor.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view - supports both session and token-based logout"""
    # Handle AJAX/JSON requests
    if request.method == 'POST' and request.headers.get('Content-Type') == 'application/json':
        try:
            # Get refresh token if available
            data = json.loads(request.body)
            refresh_token = data.get('refresh_token')
            
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except Exception:
                    pass
            
            logout(request)
            return JsonResponse({'success': True, 'message': 'Successfully logged out'})
        except Exception as e:
            logout(request)
            return JsonResponse({'success': True, 'message': 'Successfully logged out'})
    
    # Traditional logout
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('core:index')


def index(request):
    """Landing page"""
    return render(request, 'index.html')


def chat_view(request):
    """Anonymous chatbot interface"""
    return render(request, 'chat.html')


@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """Process chat messages and return responses with emotion integration"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        session_id_str = data.get('session_id', '')
        emotion = data.get('emotion', None)  # New: Receive emotion from frontend
<<<<<<< HEAD
        preferred_language = data.get('language', 'en')  # Language preference from frontend
=======
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a

        if not message:
            return JsonResponse({'error': 'Message is required'}, status=400)

        # Get or create chat session
        if session_id_str:
            try:
                session_id = uuid.UUID(session_id_str)
                chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid session ID'}, status=400)
        else:
            # Create new session
            chat_session = ChatSession.objects.create()
            session_id = chat_session.session_id

        # Get chat history
        recent_messages = ChatMessage.objects.filter(session=chat_session).order_by('timestamp')[:10]
        session_history = [(msg.message, msg.response) for msg in recent_messages]

<<<<<<< HEAD
        # Get chatbot response with emotion context and language preference
        response_data = get_chatbot_response(message, session_history, emotion, preferred_language)
=======
        # Get chatbot response with emotion context
        response_data = get_chatbot_response(message, session_history, emotion)
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a

        # Analyze sentiment
        sentiment_score = analyze_sentiment(message)

        # Save message and response
        chat_message = ChatMessage.objects.create(
            session=chat_session,
            message=message,
            response=response_data['response'],
            sentiment_score=sentiment_score
        )

        # Update analytics
        today = date.today()
        analytics, created = Analytics.objects.get_or_create(date=today)
        analytics.total_sessions = ChatSession.objects.filter(created_at__date=today).count()

        # Check for keywords
        keywords = extract_keywords(message)
        if 'anxiety' in keywords:
            analytics.anxiety_keywords += 1
        if 'depression' in keywords:
            analytics.depression_keywords += 1

        analytics.save(update_fields=['total_sessions', 'anxiety_keywords', 'depression_keywords'])

        # Prepare response
        result = {
            'response': response_data['response'],
            'session_id': str(session_id),
            'crisis_detected': response_data['crisis_detected'],
            'suggested_action': response_data['suggested_action'],
            'timestamp': chat_message.timestamp.isoformat(),
            'emotion_context': response_data.get('emotion_context', '')  # Include emotion context for debugging
        }

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def appointments_view(request):
    """Appointment booking page"""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            # Try to get session from localStorage (if coming from chat)
            session_id_str = request.POST.get('session_id', '')
            if session_id_str:
                try:
                    session_id = uuid.UUID(session_id_str)
                    chat_session = ChatSession.objects.filter(session_id=session_id).first()
                    if chat_session:
                        appointment.session = chat_session
                except ValueError:
                    pass
            
            appointment.save()
            
            # Update analytics
            today = date.today()
            analytics, created = Analytics.objects.get_or_create(date=today)
            analytics.appointments_booked += 1
            analytics.save()
            
            messages.success(request, f'Appointment booked successfully for {appointment.appointment_date.strftime("%B %d, %Y at %I:%M %p")}!')
            return redirect('core:appointments')
    else:
        form = AppointmentForm()
    
    # Get available counselors
    counselors = CustomUser.objects.filter(role='counselor')
    
    return render(request, 'appointments.html', {
        'form': form,
        'counselors': counselors
    })


@login_required
def appointments_manage(request):
    """List all appointments for admin/counselor"""
    user = request.user
    if user.role not in ['admin', 'counselor']:
        messages.error(request, 'Access denied. Admin/Counselor access required.')
        return redirect('core:index')
    
    if user.role == 'counselor':
        appointments = Appointment.objects.filter(counselor=user).order_by('-appointment_date')
    else:  # admin
        appointments = Appointment.objects.all().order_by('-appointment_date')
    
    return render(request, 'appointments_manage.html', {
        'appointments': appointments
    })


@csrf_exempt
@require_http_methods(["POST"])
def appointment_update(request, appointment_id):
    """Update appointment status - supports both session and token auth"""
    # Support both session and token authentication
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        user = request.user
        
        # Check permissions
        if user.role not in ['admin', 'counselor']:
            return JsonResponse({'error': 'Permission denied. Admin or Counselor access required.'}, status=403)
        if user.role == 'counselor' and appointment.counselor != user:
            return JsonResponse({'error': 'Permission denied. You can only update your own appointments.'}, status=403)
        
        data = json.loads(request.body)
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if not new_status:
            return JsonResponse({'error': 'Status is required'}, status=400)
        
        valid_statuses = [choice[0] for choice in Appointment.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return JsonResponse({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}, status=400)
        
        appointment.status = new_status
        if notes:
            appointment.notes = notes
        appointment.save()
        return JsonResponse({'success': True, 'status': appointment.status})
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def resources_view(request):
    """Resources page with filtering"""
    resources = Resource.objects.all()
    
    # Filter by type
    resource_type = request.GET.get('type', '')
    if resource_type:
        resources = resources.filter(type=resource_type)
    
    # Filter by language
    language = request.GET.get('language', '')
    if language:
        resources = resources.filter(language=language)
    
    return render(request, 'resources.html', {
        'resources': resources,
        'selected_type': resource_type,
        'selected_language': language,
    })


def forum_view(request):
    """Peer support forum - list approved posts"""
    posts = ForumPost.objects.filter(moderated=True).order_by('-timestamp')
<<<<<<< HEAD
    
    # Get session ID to check likes
    session_id_str = request.GET.get('session_id', '') or request.session.get('session_id', '')
    liked_post_ids = set()
    
    if session_id_str:
        try:
            session_id = uuid.UUID(session_id_str)
            chat_session = ChatSession.objects.filter(session_id=session_id).first()
            if chat_session:
                liked_post_ids = set(
                    ForumPostLike.objects.filter(session=chat_session, post__in=posts)
                    .values_list('post_id', flat=True)
                )
        except ValueError:
            pass
    
    return render(request, 'forum.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids
    })
=======
    return render(request, 'forum.html', {'posts': posts})
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a


@csrf_exempt
@require_http_methods(["POST"])
def forum_post_create(request):
    """Create anonymous forum post"""
    try:
        data = json.loads(request.body)
        session_id_str = data.get('session_id', '')
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)
        
        # Get or create session
        if session_id_str:
            try:
                session_id = uuid.UUID(session_id_str)
                chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid session ID'}, status=400)
        else:
            chat_session = ChatSession.objects.create()
        
        # Create post (initially not moderated)
        post = ForumPost.objects.create(
            session=chat_session,
            title=title,
            content=content,
            moderated=False
        )
        
        return JsonResponse({
            'success': True,
            'post_id': post.id,
            'message': 'Your post has been submitted and is pending moderation. It will appear once approved.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def forum_post_detail(request, post_id):
    """Get forum post with replies"""
    post = get_object_or_404(ForumPost, id=post_id, moderated=True)
    replies = ForumReply.objects.filter(post=post, moderated=True).order_by('timestamp')
<<<<<<< HEAD
    
    # Check if current session has liked this post
    session_id_str = request.GET.get('session_id', '') or request.session.get('session_id', '')
    is_liked = False
    if session_id_str:
        try:
            session_id = uuid.UUID(session_id_str)
            chat_session = ChatSession.objects.filter(session_id=session_id).first()
            if chat_session:
                is_liked = ForumPostLike.objects.filter(post=post, session=chat_session).exists()
        except ValueError:
            pass
    
    return render(request, 'forum_post_detail.html', {
        'post': post, 
        'replies': replies,
        'is_liked': is_liked
    })


@csrf_exempt
@require_http_methods(["POST"])
def forum_post_like(request, post_id):
    """Like or unlike a forum post"""
    try:
        post = get_object_or_404(ForumPost, id=post_id, moderated=True)
        data = json.loads(request.body)
        session_id_str = data.get('session_id', '')
        
        if not session_id_str:
            return JsonResponse({'error': 'Session ID is required'}, status=400)
        
        try:
            session_id = uuid.UUID(session_id_str)
            chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid session ID'}, status=400)
        
        # Check if already liked
        try:
            like = ForumPostLike.objects.get(post=post, session=chat_session)
            # Like already exists, so unlike (delete)
            like.delete()
            # Refresh post to get updated count
            post.refresh_from_db()
            return JsonResponse({
                'success': True,
                'liked': False,
                'likes_count': post.likes_count,
                'message': 'Post unliked successfully'
            })
        except ForumPostLike.DoesNotExist:
            # Like doesn't exist, create it
            ForumPostLike.objects.create(post=post, session=chat_session)
            # Refresh post to get updated count
            post.refresh_from_db()
            return JsonResponse({
                'success': True,
                'liked': True,
                'likes_count': post.likes_count,
                'message': 'Post liked successfully'
            })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def forum_post_share(request, post_id):
    """Track share of a forum post"""
    try:
        post = get_object_or_404(ForumPost, id=post_id, moderated=True)
        data = json.loads(request.body)
        session_id_str = data.get('session_id', '')
        share_platform = data.get('platform', '')
        
        if not session_id_str:
            return JsonResponse({'error': 'Session ID is required'}, status=400)
        
        try:
            session_id = uuid.UUID(session_id_str)
            chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid session ID'}, status=400)
        
        # Create share record
        share = ForumPostShare.objects.create(
            post=post,
            session=chat_session,
            share_platform=share_platform
        )
        
        return JsonResponse({
            'success': True,
            'shares_count': post.shares_count,
            'message': 'Share recorded successfully',
            'share_url': request.build_absolute_uri(f'/forum/post/{post_id}/')
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
=======
    return render(request, 'forum_post_detail.html', {'post': post, 'replies': replies})
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a


@csrf_exempt
@require_http_methods(["POST"])
def forum_reply_create(request, post_id):
    """Create reply to forum post"""
    try:
        # Check if post exists (can be moderated or not)
        try:
            post = ForumPost.objects.get(id=post_id)
        except ForumPost.DoesNotExist:
            return JsonResponse({'error': 'Post not found'}, status=404)
        
        data = json.loads(request.body)
        session_id_str = data.get('session_id', '')
        content = data.get('content', '').strip()
        
        if not content:
            return JsonResponse({'error': 'Content is required'}, status=400)
        
        # Get or create session
        if session_id_str:
            try:
                session_id = uuid.UUID(session_id_str)
                chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid session ID'}, status=400)
        else:
            chat_session = ChatSession.objects.create()
        
        # Create reply (initially not moderated)
        reply = ForumReply.objects.create(
            post=post,
            session=chat_session,
            content=content,
            moderated=False
        )
        
        # Update replies count
        post.replies_count = ForumReply.objects.filter(post=post, moderated=True).count()
        post.save()
        
        return JsonResponse({
            'success': True,
            'reply_id': reply.id,
            'message': 'Your reply has been submitted and is pending moderation.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def forum_moderate(request):
    """Get posts and replies needing moderation"""
    posts = ForumPost.objects.filter(moderated=False).order_by('-timestamp')
    replies = ForumReply.objects.filter(moderated=False).order_by('-timestamp')
    return render(request, 'forum_moderate.html', {'posts': posts, 'replies': replies})


@csrf_exempt
@require_http_methods(["POST"])
def forum_approve(request, item_type, item_id):
    """Approve forum post or reply - supports both session and token auth"""
    # Support both session and token authentication
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user = request.user
    if user.role != 'admin':
        return JsonResponse({'error': 'Permission denied. Admin access required.'}, status=403)
    
    try:
        if item_type == 'post':
            item = get_object_or_404(ForumPost, id=item_id)
        elif item_type == 'reply':
            item = get_object_or_404(ForumReply, id=item_id)
        else:
            return JsonResponse({'error': 'Invalid item type. Must be "post" or "reply"'}, status=400)
        
        item.moderated = True
        item.save()
        
        # Update replies count if approving a post
        if item_type == 'post':
            item.replies_count = ForumReply.objects.filter(post=item, moderated=True).count()
            item.save()
        
        return JsonResponse({'success': True, 'message': f'{item_type.capitalize()} approved successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def forum_delete(request, item_type, item_id):
    """Delete inappropriate forum post or reply (token-based)"""
    user = request.user
    if user.role != 'admin':
        return Response(
            {'error': 'Permission denied. Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        if item_type == 'post':
            item = get_object_or_404(ForumPost, id=item_id)
        elif item_type == 'reply':
            item = get_object_or_404(ForumReply, id=item_id)
        else:
            return Response(
                {'error': 'Invalid item type. Must be "post" or "reply"'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        item_type_name = item_type
        item.delete()
        return Response(
            {'success': True, 'message': f'{item_type_name.capitalize()} deleted successfully'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def dashboard_view(request):
    """Admin dashboard with analytics"""
    user = request.user
    if user.role not in ['admin', 'counselor']:
        messages.error(request, 'Access denied. Admin/Counselor access required.')
        return redirect('core:index')
    if user.role == 'counselor' and not user.is_verified:
        messages.error(request, 'Your counselor account is pending verification.')
        return redirect('core:index')
    
    # Get recent analytics (last 30 days)
    from datetime import timedelta
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_analytics = Analytics.objects.filter(date__gte=thirty_days_ago).order_by('date')
    
    # Calculate totals
    total_sessions = ChatSession.objects.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    unmoderated_posts = ForumPost.objects.filter(moderated=False).count()
    unmoderated_replies = ForumReply.objects.filter(moderated=False).count()
    
    # Recent appointments
    recent_appointments = Appointment.objects.order_by('-appointment_date')[:10]
    
    # Prepare chart data as JSON string for template
    import json as json_module
    chart_data_json = json_module.dumps({
        'dates': [str(a.date) for a in recent_analytics],
        'sessions': [a.total_sessions for a in recent_analytics],
        'anxiety': [a.anxiety_keywords for a in recent_analytics],
        'depression': [a.depression_keywords for a in recent_analytics],
        'appointments': [a.appointments_booked for a in recent_analytics],
    })
    
    return render(request, 'dashboard.html', {
        'total_sessions': total_sessions,
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'unmoderated_posts': unmoderated_posts,
        'unmoderated_replies': unmoderated_replies,
        'recent_appointments': recent_appointments,
        'chart_data': chart_data_json,
    })


@login_required
def dashboard_stats_api(request):
    """JSON endpoint for dashboard stats"""
    user = request.user
    if user.role not in ['admin', 'counselor']:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    from datetime import timedelta
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_analytics = Analytics.objects.filter(date__gte=thirty_days_ago).order_by('date')
    
    stats = {
        'total_sessions': ChatSession.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'unmoderated_posts': ForumPost.objects.filter(moderated=False).count(),
        'chart_data': {
            'dates': [str(a.date) for a in recent_analytics],
            'sessions': [a.total_sessions for a in recent_analytics],
            'anxiety': [a.anxiety_keywords for a in recent_analytics],
            'depression': [a.depression_keywords for a in recent_analytics],
        }
    }
    
    return JsonResponse(stats)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that uses CustomTokenObtainPairSerializer"""
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def api_login(request):
    """Token-based login API endpoint"""
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Get user info
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_verified': user.is_verified if hasattr(user, 'is_verified') else False,
        }
        
        return Response({
            'access': access_token,
            'refresh': refresh_token,
            'user': user_data
        }, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def api_logout(request):
    """Token-based logout API endpoint"""
    try:
        # Get refresh token from request body or header
        refresh_token = None
        if request.data:
            refresh_token = request.data.get('refresh_token')
        elif hasattr(request, 'body'):
            try:
                data = json.loads(request.body)
                refresh_token = data.get('refresh_token')
            except:
                pass
        
        # Try to blacklist if token provided (optional)
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                # If blacklist is not configured, just pass
                pass
        
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@csrf_exempt
@require_http_methods(["POST"])
def predict_emotion_api(request):
    """FER prediction API endpoint - processes image bytes and returns emotion"""
    try:
        # Get the uploaded image file
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image file provided'}, status=400)

        image_file = request.FILES['image']

        # Read image bytes
        image_bytes = image_file.read()

        # Import the prediction function
<<<<<<< HEAD
        import sys
        import os
        # Add the project root to the path to find predict_emotion module
        # views.py is in core/, so we need to go up one level to get to project root
        current_dir = os.path.dirname(os.path.abspath(__file__))  # core/
        project_root = os.path.dirname(current_dir)  # CU_HACKATHON/
        
        if project_root not in sys.path:
            sys.path.insert(0, project_root)
        
        try:
            from predict_emotion import predict_emotion_from_image
        except ImportError as e:
            # Fallback: try direct import
            import importlib.util
            predict_path = os.path.join(project_root, 'predict_emotion.py')
            if os.path.exists(predict_path):
                spec = importlib.util.spec_from_file_location("predict_emotion", predict_path)
                predict_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(predict_module)
                predict_emotion_from_image = predict_module.predict_emotion_from_image
            else:
                raise ImportError(f"Could not find predict_emotion.py at {predict_path}. Original error: {str(e)}")
=======
        from predict_emotion import predict_emotion_from_image
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a

        # Get emotion prediction
        emotion = predict_emotion_from_image(image_bytes)

        return JsonResponse({
            'emotion': emotion,
            'success': True
        })

    except Exception as e:
<<<<<<< HEAD
        import traceback
        from django.conf import settings
        error_details = traceback.format_exc()
        print(f"Emotion prediction error: {error_details}")  # Log for debugging
        return JsonResponse({
            'error': str(e),
            'emotion': 'Decode_Error',
            'details': error_details if settings.DEBUG else None
        }, status=500)


def checkin_view(request):
    """1-Minute Anonymous Check-in quiz interface"""
    return render(request, 'checkin.html')


@csrf_exempt
@require_http_methods(["POST"])
def checkin_api(request):
    """Process check-in quiz responses and calculate score"""
    try:
        data = json.loads(request.body)
        responses = data.get('responses', [])
        session_id_str = data.get('session_id', '')

        if not responses or len(responses) != 5:
            return JsonResponse({'error': 'All 5 questions must be answered'}, status=400)

        # Calculate total score
        total_score = sum(responses)

        # Determine bucket
        if total_score <= 4:
            bucket = 1  # Green/Mild
        elif total_score <= 9:
            bucket = 2  # Yellow/Moderate
        else:
            bucket = 3  # Red/High

        # Get or create chat session for tracking
        if session_id_str:
            try:
                session_id = uuid.UUID(session_id_str)
                chat_session, created = ChatSession.objects.get_or_create(session_id=session_id)
            except ValueError:
                chat_session = ChatSession.objects.create()
        else:
            chat_session = ChatSession.objects.create()

        # Store check-in result (you might want to create a model for this)
        # For now, we'll store in session
        request.session['checkin_score'] = total_score
        request.session['checkin_bucket'] = bucket
        request.session['checkin_session_id'] = str(chat_session.session_id)

        return JsonResponse({
            'score': total_score,
            'bucket': bucket,
            'session_id': str(chat_session.session_id),
            'success': True
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def checkin_results_view(request):
    """Display check-in results based on score bucket"""
    score = request.session.get('checkin_score')
    bucket = request.session.get('checkin_bucket')
    session_id = request.session.get('checkin_session_id')

    if score is None or bucket is None:
        # Redirect to check-in if no results
        return redirect('core:checkin')

    context = {
        'score': score,
        'bucket': bucket,
        'session_id': session_id,
    }

    return render(request, 'checkin_results.html', context)
=======
        return JsonResponse({
            'error': str(e),
            'emotion': 'Decode_Error'
        }, status=500)
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
