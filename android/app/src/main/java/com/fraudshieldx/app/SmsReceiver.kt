package com.fraudshieldx.app
import android.content.*
import android.provider.Telephony
import org.json.JSONObject
class SmsReceiver:BroadcastReceiver(){override fun onReceive(c:Context,i:Intent){if(i.action!=Telephony.Sms.Intents.SMS_RECEIVED_ACTION)return;for(s in Telephony.Sms.Intents.getMessagesFromIntent(i)){val body=s.messageBody?:continue;ApiClient.analyze(body,s.originatingAddress){raw->if(raw!=null)try{val j=JSONObject(raw);val l=j.getString("risk_level");if(l=="HIGH"||l=="MEDIUM")AlertHelper.show(c,j.getInt("risk_score"),l,j.getString("recommendation"))}catch(_:Exception){}}}}}
