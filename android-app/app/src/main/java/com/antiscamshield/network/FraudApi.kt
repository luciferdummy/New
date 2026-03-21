package com.antiscamshield.network

import com.antiscamshield.BuildConfig
import com.antiscamshield.model.PaymentEvent
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path

data class AnalyzeTransactionRequest(
    val amount: Double?,
    val receiver: String?,
    val upi_id: String?,
    val source: String,
    val message: String?,
    val has_otp_context: Boolean,
    val is_collect_request: Boolean,
    val is_autopay: Boolean,
    val hour_of_day: Int,
    val average_amount: Double,
    val recent_transaction_count: Int,
    val known_contacts: List<String>,
    val blacklisted_upi_ids: List<String>
)

data class AnalyzeMessageRequest(val message: String)

data class RiskApiResponse(
    val risk_score: Int,
    val risk_level: String,
    val reason: List<String>
)

interface FraudApi {
    @POST("/analyze_transaction")
    suspend fun analyzeTransaction(@Body request: AnalyzeTransactionRequest): RiskApiResponse

    @POST("/analyze_message")
    suspend fun analyzeMessage(@Body request: AnalyzeMessageRequest): RiskApiResponse

    @GET("/blacklist_check/{upiId}")
    suspend fun blacklistCheck(@Path("upiId") upiId: String): Map<String, Any>

    companion object {
        val instance: FraudApi by lazy {
            Retrofit.Builder()
                .baseUrl(BuildConfig.API_BASE_URL)
                .addConverterFactory(GsonConverterFactory.create())
                .build()
                .create(FraudApi::class.java)
        }
    }
}
