package com.fraudshieldx.app
import android.Manifest
import android.app.Activity
import android.os.Bundle
import android.content.pm.PackageManager
import android.widget.*
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
class MainActivity:Activity(){override fun onCreate(b:Bundle?){super.onCreate(b);val l=LinearLayout(this);l.orientation=LinearLayout.VERTICAL;l.setPadding(40,60,40,40);val t=TextView(this);t.text="🛡️ FraudShield X\n\nProactive SMS scam detection";t.textSize=24f;l.addView(t);val btn=Button(this);btn.text="Enable SMS Detection";btn.setOnClickListener{ask()};l.addView(btn);setContentView(l);ask()}private fun ask(){val p=arrayOf(Manifest.permission.RECEIVE_SMS,Manifest.permission.READ_SMS,Manifest.permission.POST_NOTIFICATIONS);val m=p.filter{ContextCompat.checkSelfPermission(this,it)!=PackageManager.PERMISSION_GRANTED};if(m.isNotEmpty())ActivityCompat.requestPermissions(this,m.toTypedArray(),10)}}
