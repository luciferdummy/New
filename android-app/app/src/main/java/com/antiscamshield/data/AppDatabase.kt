package com.antiscamshield.data

import android.content.Context
import androidx.room.Dao
import androidx.room.Database
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Room
import androidx.room.RoomDatabase
import com.antiscamshield.model.BlacklistedUpi
import com.antiscamshield.model.KnownContact
import com.antiscamshield.model.RiskLog
import com.antiscamshield.model.TransactionLog

@Dao
interface AntiScamDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertTransaction(log: TransactionLog)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertRiskLog(log: RiskLog)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertContact(contact: KnownContact)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertBlacklist(item: BlacklistedUpi)

    @Query("SELECT * FROM transaction_logs ORDER BY createdAt DESC LIMIT 50")
    suspend fun recentTransactions(): List<TransactionLog>

    @Query("SELECT AVG(amount) FROM transaction_logs")
    suspend fun averageAmount(): Double?

    @Query("SELECT COUNT(*) FROM transaction_logs WHERE createdAt > :afterMillis")
    suspend fun countTransactionsAfter(afterMillis: Long): Int

    @Query("SELECT * FROM known_contacts")
    suspend fun contacts(): List<KnownContact>

    @Query("SELECT * FROM blacklisted_upi_ids")
    suspend fun blacklist(): List<BlacklistedUpi>
}

@Database(
    entities = [TransactionLog::class, KnownContact::class, BlacklistedUpi::class, RiskLog::class],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun antiScamDao(): AntiScamDao

    companion object {
        fun build(context: Context): AppDatabase = Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "anti_scam_shield.db"
        ).fallbackToDestructiveMigration().build()
    }
}
