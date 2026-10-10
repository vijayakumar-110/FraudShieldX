package com.fraudshieldx.app
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.Executors
object ApiClient { private val client=OkHttpClient(); private val ex=Executors.newSingleThreadExecutor(); fun analyze(message:String,sender:String?,cb:(String?)->Unit){ex.execute{try{val j=JSONObject().put("message",message).put("source","android_sms").put("sender",sender? : "");val req=Request.Builder().url(NetworkConfig.BASE_URL+"/api/analyze").post(j.toString().toRequestBody("application/json".toMediaType())).build();client.newCall(req).execute().use{cb(if(it.isSuccessful)it.body?.string() else null)}}catch(_:Exception){cb(null)}}}}
