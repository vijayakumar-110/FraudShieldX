package com.fraudshieldx.app
import android.app.*
import android.content.Context
import androidx.core.app.NotificationCompat
object AlertHelper { private const val CH="fraud_alerts"; fun show(c:Context,score:Int,level:String,rec:String){val m=c.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager;m.createNotificationChannel(NotificationChannel(CH,"Fraud Alerts",NotificationManager.IMPORTANCE_HIGH));val n=NotificationCompat.Builder(c,CH).setSmallIcon(android.R.drawable.ic_dialog_alert).setContentTitle(if(level=="HIGH")"🚨 Possible Scam Detected" else "⚠️ Suspicious Message").setContentText("Risk $score/100").setStyle(NotificationCompat.BigTextStyle().bigText(rec)).setPriority(NotificationCompat.PRIORITY_HIGH).setAutoCancel(true).build();m.notify((System.currentTimeMillis()%100000).toInt(),n)}}
