package com.antiscamshield.model

import androidx.room.Entity
import androidx.room.PrimaryKey

enum class RiskLevel { SAFE, SUSPICIOUS, HIGH }
enum class MessageCategory { OTP, DEBIT, CREDIT, SCAM, PROMOTION, UNKNOWN }

data class PaymentEvent(
    val source: String,
    val appPackage: String? = null,
    val amount: Double? = null,
    val upiId: String? = null,
    val receiver: String? = null,
    val message: String? = null,
    val hasOtpContext: Boolean = false,
    val isCollectRequest: Boolean = false,
    val isAutopay: Boolean = false,
    val timestamp: Long = System.currentTimeMillis()
)

data class RiskAssessment(
    val riskScore: Int,
    val riskLevel: RiskLevel,
    val reasons: List<String>
)

@Entity(tableName = "transaction_logs")
data class TransactionLog(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val receiver: String,
    val upiId: String,
    val amount: Double,
    val riskScore: Int,
    val riskLevel: String,
    val reasons: String,
    val createdAt: Long = System.currentTimeMillis()
)

@Entity(tableName = "known_contacts")
data class KnownContact(
    @PrimaryKey val upiId: String,
    val displayName: String,
    val lastSeenAt: Long = System.currentTimeMillis()
)

@Entity(tableName = "blacklisted_upi_ids")
data class BlacklistedUpi(
    @PrimaryKey val upiId: String,
    val reason: String
)

@Entity(tableName = "risk_logs")
data class RiskLog(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val source: String,
    val payloadSummary: String,
    val riskScore: Int,
    val reasons: String,
    val createdAt: Long = System.currentTimeMillis()
)

data class SmsAnalysis(
    val category: MessageCategory,
    val amount: Double?,
    val extractedKeywords: List<String>,
    val suspiciousLink: Boolean,
    val otpDetected: Boolean
)
