# -*- coding: utf-8 -*-
# (c) YashDK [yash-dk@github]

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin,ChannelParticipantCreator,ChannelParticipantsAdmins
import logging,traceback
from ..core.getVars import get_val
torlog = logging.getLogger(__name__)

#todo add alpha admin if needed

async def is_admin(client,user_id,chat_id):
    try:
        res = await client(GetParticipantRequest(
            channel=chat_id,
            user_id=user_id
        ))

        try:
            if isinstance(res.participant,(ChannelParticipantAdmin,ChannelParticipantCreator,ChannelParticipantsAdmins)):
                return True
            else:
                
                return user_id in get_val("ALD_USR")
        except:
            torlog.error(f"Error in admin check {traceback.format_exc()}")
            return False
    except Exception as e:
        torlog.error(f"Error in admin check {e}")
        return user_id in get_val("ALD_USR")