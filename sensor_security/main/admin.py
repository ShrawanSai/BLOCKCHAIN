from django.contrib import admin
from .models import Block, Chain,Transactions,Data

admin.site.register(Block)
admin.site.register(Chain)
admin.site.register(Transactions)
admin.site.register(Data)
