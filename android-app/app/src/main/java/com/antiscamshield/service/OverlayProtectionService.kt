package com.antiscamshield.service

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.os.Build
import android.os.IBinder
import com.antiscamshield.overlay.OverlayController
import com.antiscamshield.model.RiskAssessment
import com.antiscamshield.model.RiskLevel

class OverlayProtectionService : Service() {
    private lateinit var controller: OverlayController

    override fun onCreate() {
        super.onCreate()
        controller = OverlayController(this)
        startForeground(1001, buildNotification())
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val score = intent?.getIntExtra("riskScore", 70) ?: 70
        val level = intent?.getStringExtra("riskLevel") ?: RiskLevel.HIGH.name
        val reasons = intent?.getStringArrayListExtra("reasons")?.toList().orEmpty()
        controller.show(
            RiskAssessment(score, RiskLevel.valueOf(level), reasons),
            onCancel = { stopSelf() },
            onProceed = { stopSelf() }
        )
        return START_NOT_STICKY
    }

    override fun onDestroy() {
        controller.dismiss()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun buildNotification(): Notification {
        val manager = getSystemService(NotificationManager::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            manager.createNotificationChannel(
                NotificationChannel("overlay", "Overlay Protection", NotificationManager.IMPORTANCE_LOW)
            )
        }
        return Notification.Builder(this, "overlay")
            .setContentTitle("Anti-Scam Shield active")
            .setContentText("Monitoring payment screens for risky behavior")
            .setSmallIcon(android.R.drawable.ic_dialog_alert)
            .build()
    }
}
