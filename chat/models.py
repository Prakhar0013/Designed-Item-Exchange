from django.db import models
from django.contrib.auth.models import User
from items.models import Item

class ChatRoom(models.Model):
    """ Represents a conversation between two users about a specific item """
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='chat_rooms')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='started_chats')
    # Seller is implicitly item.owner
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure only one chat room per buyer per item
        unique_together = ('item', 'buyer')

    def __str__(self):
        return f"Chat about '{self.item.name}' between {self.buyer.username} and {self.item.owner.username}"

    def get_seller(self):
        return self.item.owner

    def get_participants(self):
        return [self.buyer, self.item.owner]
    
    def get_other_participant(self, user):
        """
        Given one participant (user), returns the other participant.
        """
        if user == self.buyer:
            return self.item.owner # Seller
        elif user == self.item.owner:
            return self.buyer
        else:
            # Should not happen if view logic is correct, but good practice
            return None


class Message(models.Model):
    """ A message within a chat room """
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # Show newest messages last

    def __str__(self):
        return f"Msg by {self.sender.username} in Room {self.room.id} at {self.timestamp}"