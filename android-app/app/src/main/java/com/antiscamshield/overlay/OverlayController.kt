package com.antiscamshield.overlay

import android.content.Context
import android.graphics.PixelFormat
import android.os.Build
import android.os.CountDownTimer
import android.speech.tts.TextToSpeech
import android.view.Gravity
import android.view.LayoutInflater
import android.view.View
import android.view.WindowManager
import android.widget.Button
import android.widget.TextView
import com.antiscamshield.R
import com.antiscamshield.model.RiskAssessment
import java.util.Locale

class OverlayController(private val context: Context) : TextToSpeech.OnInitListener {
    private val windowManager = context.getSystemService(Context.WINDOW_SERVICE) as WindowManager
    private var overlayView: View? = null
    private var textToSpeech: TextToSpeech = TextToSpeech(context, this)

    fun show(assessment: RiskAssessment, onCancel: () -> Unit, onProceed: () -> Unit) {
        if (overlayView != null) return
        val inflater = LayoutInflater.from(context)
        val view = inflater.inflate(R.layout.overlay_warning, null)
        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else WindowManager.LayoutParams.TYPE_PHONE,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT
        ).apply { gravity = Gravity.TOP }

        view.findViewById<TextView>(R.id.riskTitle).text = "${assessment.riskLevel} RISK • ${assessment.riskScore}/100"
        view.findViewById<TextView>(R.id.reasonText).text = assessment.reasons.joinToString("\n• ", prefix = "• ")
        val timerText = view.findViewById<TextView>(R.id.countdownText)
        view.findViewById<Button>(R.id.cancelButton).setOnClickListener {
            dismiss()
            onCancel()
        }
        view.findViewById<Button>(R.id.proceedButton).setOnClickListener {
            dismiss()
            onProceed()
        }

        object : CountDownTimer(8000, 1000) {
            override fun onTick(millisUntilFinished: Long) {
                timerText.text = "Please wait ${millisUntilFinished / 1000}s before proceeding"
            }
            override fun onFinish() {
                timerText.text = "You may proceed, but verify the receiver carefully"
            }
        }.start()

        overlayView = view
        windowManager.addView(view, params)
        speakWarning()
    }

    fun dismiss() {
        overlayView?.let { windowManager.removeView(it) }
        overlayView = null
    }

    private fun speakWarning() {
        textToSpeech.speak(
            "This transaction may be a scam. Please verify before proceeding.",
            TextToSpeech.QUEUE_FLUSH,
            null,
            "risk-warning"
        )
    }

    override fun onInit(status: Int) {
        textToSpeech.language = Locale.US
    }
}
