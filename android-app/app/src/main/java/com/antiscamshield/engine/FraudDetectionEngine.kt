package com.antiscamshield.engine

import com.antiscamshield.data.AppRepository
import com.antiscamshield.model.MessageCategory
import com.antiscamshield.model.PaymentEvent
import com.antiscamshield.model.RiskAssessment
import com.antiscamshield.model.RiskLevel
import com.antiscamshield.model.SmsAnalysis
import com.antiscamshield.network.AnalyzeTransactionRequest
import com.antiscamshield.network.FraudApi
import java.util.Calendar

class FraudDetectionEngine(
    private val repository: AppRepository,
    private val api: FraudApi = FraudApi.instance
) {
    private val scamKeywords = listOf("refund", "urgent", "verify", "suspended", "collect", "reward", "kyc")

    suspend fun analyzeEvent(event: PaymentEvent): RiskAssessment {
        val averageAmount = repository.averageAmount()
        val contacts = repository.contacts().map { it.upiId.lowercase() }
        val blacklist = repository.blacklist().map { it.upiId.lowercase() }
        val transactionCount = repository.recentTransactionCount(System.currentTimeMillis() - 60 * 60 * 1000)

        var score = 0
        val reasons = mutableListOf<String>()

        val amount = event.amount ?: 0.0
        val upiId = (event.upiId ?: "").lowercase()
        val receiverLabel = (event.receiver ?: upiId).ifBlank { "unknown receiver" }
        val hour = Calendar.getInstance().get(Calendar.HOUR_OF_DAY)

        if (amount > averageAmount * 3 && amount > 0) {
            score += 25
            reasons += "Unusual amount compared with recent behavior"
        }
        if (upiId.isNotBlank() && upiId !in contacts) {
            score += 20
            reasons += "Receiver is not in known contacts"
        }
        if (event.message.orEmpty().contains(Regex("bit\\.ly|tinyurl|goo\\.gl", RegexOption.IGNORE_CASE))) {
            score += 20
            reasons += "Suspicious short link detected"
        }
        if (event.message != null && scamKeywords.any { event.message.contains(it, true) }) {
            score += 15
            reasons += "Scam language found in message or notification"
        }
        if (hour < 6 || hour > 23) {
            score += 10
            reasons += "Late-night transaction timing"
        }
        if (transactionCount >= 5) {
            score += 10
            reasons += "Too many recent transactions in a short window"
        }
        if (upiId.isNotBlank() && upiId in blacklist) {
            score += 35
            reasons += "UPI ID appears in blacklist"
        }
        if (event.hasOtpContext) {
            score += 15
            reasons += "OTP received before transaction attempt"
        }
        if (event.isCollectRequest) {
            score += 20
            reasons += "Collect request approval detected"
        }
        if (event.isAutopay) {
            score += 10
            reasons += "Autopay approval can hide recurring scam charges"
        }

        val remote = runCatching {
            api.analyzeTransaction(
                AnalyzeTransactionRequest(
                    amount = event.amount,
                    receiver = receiverLabel,
                    upi_id = event.upiId,
                    source = event.source,
                    message = event.message,
                    has_otp_context = event.hasOtpContext,
                    is_collect_request = event.isCollectRequest,
                    is_autopay = event.isAutopay,
                    hour_of_day = hour,
                    average_amount = averageAmount,
                    recent_transaction_count = transactionCount,
                    known_contacts = contacts,
                    blacklisted_upi_ids = blacklist
                )
            )
        }.getOrNull()

        if (remote != null) {
            score = maxOf(score, remote.risk_score)
            reasons += remote.reason
        }

        val clamped = score.coerceIn(0, 100)
        val level = when (clamped) {
            in 0..30 -> RiskLevel.SAFE
            in 31..60 -> RiskLevel.SUSPICIOUS
            else -> RiskLevel.HIGH
        }
        return RiskAssessment(clamped, level, reasons.distinct())
    }

    fun analyzeSms(message: String): SmsAnalysis {
        val lower = message.lowercase()
        val category = when {
            Regex("\\botp\\b|one time password|verification code", RegexOption.IGNORE_CASE).containsMatchIn(message) -> MessageCategory.OTP
            Regex("debited|spent|paid rs|sent rs", RegexOption.IGNORE_CASE).containsMatchIn(message) -> MessageCategory.DEBIT
            Regex("credited|received rs", RegexOption.IGNORE_CASE).containsMatchIn(message) -> MessageCategory.CREDIT
            scamKeywords.any { lower.contains(it) } -> MessageCategory.SCAM
            Regex("offer|sale|discount|cashback", RegexOption.IGNORE_CASE).containsMatchIn(message) -> MessageCategory.PROMOTION
            else -> MessageCategory.UNKNOWN
        }
        val amountMatch = Regex("(?:rs\\.?|inr)\\s?([0-9,]+(?:\\.[0-9]{1,2})?)", RegexOption.IGNORE_CASE).find(message)
        val amount = amountMatch?.groupValues?.get(1)?.replace(",", "")?.toDoubleOrNull()
        val matchedKeywords = scamKeywords.filter { lower.contains(it) }
        val suspiciousLink = Regex("https?://\\S+|bit\\.ly|tinyurl", RegexOption.IGNORE_CASE).containsMatchIn(message)
        val otp = category == MessageCategory.OTP
        return SmsAnalysis(category, amount, matchedKeywords, suspiciousLink, otp)
    }
}
