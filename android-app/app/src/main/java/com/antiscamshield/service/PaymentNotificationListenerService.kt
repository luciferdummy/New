package com.antiscamshield.service

import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import com.antiscamshield.AntiScamApplication
import com.antiscamshield.engine.FraudDetectionEngine
import com.antiscamshield.model.PaymentEvent
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

class PaymentNotificationListenerService : NotificationListenerService() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    override fun onNotificationPosted(sbn: StatusBarNotification?) {
        val extras = sbn?.notification?.extras ?: return
        val title = extras.getString("android.title").orEmpty()
        val text = extras.getCharSequence("android.text")?.toString().orEmpty()
        val payload = "$title $text"
        if (!Regex("upi|collect|autopay|payment|paid|request", RegexOption.IGNORE_CASE).containsMatchIn(payload)) return

        val amount = Regex("(?:₹|Rs\\.?|INR)\\s?([0-9,]+(?:\\.[0-9]{1,2})?)", RegexOption.IGNORE_CASE)
            .find(payload)?.groupValues?.getOrNull(1)?.replace(",", "")?.toDoubleOrNull()
        val upiId = Regex("[a-zA-Z0-9._-]+@[a-zA-Z]+")
            .find(payload)?.value

        val repo = (application as AntiScamApplication).repository
        val engine = FraudDetectionEngine(repo)
        scope.launch {
            val assessment = engine.analyzeEvent(
                PaymentEvent(
                    source = "NOTIFICATION",
                    appPackage = sbn.packageName,
                    amount = amount,
                    upiId = upiId,
                    receiver = title.ifBlank { upiId },
                    message = payload,
                    isCollectRequest = payload.contains("collect", true),
                    isAutopay = payload.contains("autopay", true)
                )
            )
            repo.persistAssessment(
                PaymentEvent("NOTIFICATION", sbn.packageName, amount, upiId, title.ifBlank { upiId }, payload),
                assessment
            )
        }
    }
}
