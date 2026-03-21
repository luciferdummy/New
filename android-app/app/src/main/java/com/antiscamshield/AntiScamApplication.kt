package com.antiscamshield

import android.app.Application
import com.antiscamshield.data.AppDatabase
import com.antiscamshield.data.AppRepository

class AntiScamApplication : Application() {
    lateinit var repository: AppRepository
        private set

    override fun onCreate() {
        super.onCreate()
        val database = AppDatabase.build(this)
        repository = AppRepository(database)
    }
}
