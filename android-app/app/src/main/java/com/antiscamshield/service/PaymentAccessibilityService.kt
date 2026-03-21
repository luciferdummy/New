package com.antiscamshield.service

import android.accessibilityservice.AccessibilityService
import android.content.Intent
import android.view.accessibility.AccessibilityEvent
import android.view.accessibility.AccessibilityNodeInfo
import com.antiscamshield.AntiScamApplication
import com.antiscamshield.engine.FraudDetectionEngine
import com.antiscamshield.model.PaymentEvent
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

class PaymentAccessibilityService : AccessibilityService() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    private val engine by lazy { FraudDetectionEngine((application as AntiScamApplication).repository) }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        val root = rootInActiveWindow ?: return
        val packageName = event?.packageName?.toString() ?: return
        if (packageName !in supportedPackages) return

        val screenText = mutableListOf<String>()
        collectText(root, screenText)
        val merged = screenText.joinToString(" ")
        val amount = Regex("(?:₹|Rs\\.?|INR)\\s?([0-9,]+(?:\\.[0-9]{1,2})?)", RegexOption.IGNORE_CASE)
            .find(merged)?.groupValues?.getOrNull(1)?.replace(",", "")?.toDoubleOrNull()
        val upiId = Regex("[a-zA-Z0-9._-]+@[a-zA-Z]+")
            .find(merged)?.value
        val hasPayAction = listOf("pay", "send", "confirm").any { merged.contains(it, true) }

        if (hasPayAction && (amount != null || upiId != null)) {
            scope.launch {
                val assessment = engine.analyzeEvent(
                    PaymentEvent(
                        source = "ACCESSIBILITY",
                        appPackage = packageName,
                        amount = amount,
                        upiId = upiId,
                        receiver = upiId,
                        message = merged
                    )
                )
                if (assessment.riskScore >= 31) {
                    (application as AntiScamApplication).repository.persistAssessment(
                        PaymentEvent("ACCESSIBILITY", packageName, amount, upiId, upiId, merged),
                        assessment
                    )
                    startService(Intent(this@PaymentAccessibilityService, OverlayProtectionService::class.java).apply {
                        putExtra("riskScore", assessment.riskScore)
                        putExtra("riskLevel", assessment.riskLevel.name)
                        putStringArrayListExtra("reasons", ArrayList(assessment.reasons))
                    })
                }
            }
        }
    }

    override fun onInterrupt() = Unit

    private fun collectText(node: AccessibilityNodeInfo, collector: MutableList<String>) {
        node.text?.toString()?.let(collector::add)
        node.contentDescription?.toString()?.let(collector::add)
        for (i in 0 until node.childCount) {
            node.getChild(i)?.let { collectText(it, collector) }
        }
    }

    companion object {
        private val supportedPackages = setOf(
            "com.google.android.apps.nbu.paisa.user",
            "com.phonepe.app",
            "net.one97.paytm"
        )
    }
}
