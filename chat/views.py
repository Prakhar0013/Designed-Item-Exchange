from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import ChatRoom, Message, Item
from .forms import MessageForm
from django.db.models import Q, OuterRef, Subquery

@login_required
def start_or_go_to_chat(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    # Prevent starting chat with oneself
    if item.owner == request.user:
        # Maybe redirect back to item detail with a message?
        return redirect(item.get_absolute_url()) # Or raise Http404, or message framework

    # Find existing chat room or create a new one
    chat_room, created = ChatRoom.objects.get_or_create(
        item=item,
        buyer=request.user
    )

    return redirect('chat_room', room_id=chat_room.id)


class ChatRoomView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'chat/chat_room.html'
    form_class = MessageForm

    def get_object(self):
         # Helper method to get the chat room and cache it
        if not hasattr(self, '_chat_room'):
            self._chat_room = get_object_or_404(ChatRoom, pk=self.kwargs['room_id'])
        return self._chat_room

    def test_func(self):
        # Check if the current user is a participant in the chat room
        room = self.get_object()
        return self.request.user in room.get_participants()

    def get(self, request, *args, **kwargs):
        room = self.get_object()
        messages = room.messages.all().order_by('timestamp') # Ensure order
        form = self.form_class()
        context = {
            'room': room,
            'item': room.item,
            'messages': messages,
            'form': form,
            'other_user': room.get_seller() if request.user == room.buyer else room.buyer
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        room = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.save()
            # Redirect back to the same GET view to show the new message
            return redirect('chat_room', room_id=room.id)
        else:
            # If form is invalid, re-render the page with errors
            messages = room.messages.all().order_by('timestamp')
            context = {
                'room': room,
                'item': room.item,
                'messages': messages,
                'form': form, # Pass the invalid form back
                'other_user': room.get_seller() if request.user == room.buyer else room.buyer
            }
            return render(request, self.template_name, context)


class ChatListView(LoginRequiredMixin, View):
    template_name = 'chat/chat_list.html'

    def get(self, request, *args, **kwargs):
        # Get chat rooms where the user is either the buyer or the seller (item owner)
        user_chats = ChatRoom.objects.filter(
            Q(buyer=request.user) | Q(item__owner=request.user)
        ).select_related('item', 'buyer', 'item__owner')

        # Optional but recommended: Annotate with the timestamp of the last message for sorting
        last_message_subquery = Message.objects.filter(
            room=OuterRef('pk')
        ).order_by('-timestamp').values('timestamp')[:1]

        chat_rooms = user_chats.annotate(
            latest_message_time=Subquery(last_message_subquery)
        ).order_by('-latest_message_time', '-created_at') # Order by latest activity, then creation


        chat_list_data = []
        for room in chat_rooms:
            other_user = room.get_other_participant(request.user)
            # You could also fetch the last message content here if needed for preview
            # last_msg_obj = room.messages.last() # Be careful, potentially N+1 without prefetch_related
            chat_list_data.append({
                'room': room,
                'other_user': other_user,
                # 'last_message_preview': last_msg_obj.content[:50] if last_msg_obj else "No messages yet",
            })

        context = {
            # Pass the processed list, not the original queryset
            'chat_list_data': chat_list_data
        }
        return render(request, self.template_name, context)