package com.antiscamshield.data

import com.antiscamshield.model.KnownContact
import com.antiscamshield.model.PaymentEvent
import com.antiscamshield.model.RiskAssessment
import com.antiscamshield.model.RiskLog
import com.antiscamshield.model.TransactionLog
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AppRepository(private val database: AppDatabase) {
    private val dao = database.antiScamDao()

    suspend fun persistAssessment(event: PaymentEvent, assessment: RiskAssessment) = withContext(Dispatchers.IO) {
        val receiver = event.receiver ?: "Unknown"
        val upiId = event.upiId ?: receiver
        val amount = event.amount ?: 0.0

        dao.insertRiskLog(
            RiskLog(
                source = event.source,
                payloadSummary = "$receiver|$upiId|$amount",
                riskScore = assessment.riskScore,
                reasons = assessment.reasons.joinToString()
            )
        )

        dao.insertTransaction(
            TransactionLog(
                receiver = receiver,
                upiId = upiId,
                amount = amount,
                riskScore = assessment.riskScore,
                riskLevel = assessment.riskLevel.name,
                reasons = assessment.reasons.joinToString()
            )
        )

        dao.upsertContact(KnownContact(upiId = upiId, displayName = receiver))
    }

    suspend fun averageAmount(): Double = withContext(Dispatchers.IO) { dao.averageAmount() ?: 1000.0 }
    suspend fun recentTransactionCount(windowStart: Long): Int = withContext(Dispatchers.IO) { dao.countTransactionsAfter(windowStart) }
    suspend fun contacts() = withContext(Dispatchers.IO) { dao.contacts() }
    suspend fun blacklist() = withContext(Dispatchers.IO) { dao.blacklist() }
    suspend fun recentTransactions() = withContext(Dispatchers.IO) { dao.recentTransactions() }
}
