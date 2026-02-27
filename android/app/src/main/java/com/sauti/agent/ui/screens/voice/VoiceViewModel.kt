package com.sauti.agent.ui.screens.voice

import android.content.Context
import android.media.MediaPlayer
import android.media.MediaRecorder
import android.os.Build
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.sauti.agent.data.repository.SpeechRepository
import com.sauti.agent.data.repository.UserRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import java.io.File
import javax.inject.Inject

data class ChatMessage(val text: String, val isUser: Boolean)

sealed class VoiceUiState {
    object Idle : VoiceUiState()
    object Recording : VoiceUiState()
    object Processing : VoiceUiState()
    data class Response(val text: String) : VoiceUiState()
    data class Error(val message: String) : VoiceUiState()
}

@HiltViewModel
class VoiceViewModel @Inject constructor(
    private val speechRepository: SpeechRepository,
    private val userRepository: UserRepository,
    @ApplicationContext private val context: Context
) : ViewModel() {

    private val _uiState = MutableStateFlow<VoiceUiState>(VoiceUiState.Idle)
    val uiState: StateFlow<VoiceUiState> = _uiState.asStateFlow()

    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()

    private val _transcribedText = MutableStateFlow("")
    val transcribedText: StateFlow<String> = _transcribedText.asStateFlow()

    private var mediaRecorder: MediaRecorder? = null
    private var audioFile: File? = null
    private var mediaPlayer: MediaPlayer? = null
    private var currentTtsFile: File? = null

    fun startRecording() {
        val file = File(context.cacheDir, "voice_${System.currentTimeMillis()}.m4a")
        audioFile = file

        mediaRecorder = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            MediaRecorder(context)
        } else {
            // MediaRecorder() constructor deprecated in API 31, but required for minSdk 26 support
            @Suppress("DEPRECATION")
            MediaRecorder()
        }.apply {
            setAudioSource(MediaRecorder.AudioSource.MIC)
            setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            setOutputFile(file.absolutePath)
            prepare()
            start()
        }
        _uiState.value = VoiceUiState.Recording
    }

    fun stopRecordingAndTranscribe() {
        mediaRecorder?.apply {
            stop()
            release()
        }
        mediaRecorder = null
        _uiState.value = VoiceUiState.Processing

        viewModelScope.launch {
            val file = audioFile ?: run {
                _uiState.value = VoiceUiState.Error("No audio recorded")
                return@launch
            }
            val language = userRepository.preferredLanguage.first()
            speechRepository.transcribe(file, language)
                .onSuccess { response ->
                    _transcribedText.value = response.text
                    _messages.value += ChatMessage(response.text, isUser = true)
                    speakResponse("I heard: ${response.text}", language)
                }
                .onFailure { error ->
                    _uiState.value = VoiceUiState.Error(error.message ?: "Transcription failed")
                }
        }
    }

    private fun speakResponse(text: String, language: String) {
        viewModelScope.launch {
            speechRepository.textToSpeech(text, language)
                .onSuccess { body ->
                    _messages.value += ChatMessage(text, isUser = false)
                    _uiState.value = VoiceUiState.Response(text)
                    val ttsFile = File(context.cacheDir, "tts_${System.currentTimeMillis()}.mp3")
                    currentTtsFile = ttsFile
                    ttsFile.writeBytes(body.bytes())
                    mediaPlayer?.release()
                    mediaPlayer = MediaPlayer().apply {
                        setDataSource(ttsFile.absolutePath)
                        prepare()
                        start()
                        setOnCompletionListener {
                            ttsFile.delete()
                            _uiState.value = VoiceUiState.Idle
                        }
                    }
                }
                .onFailure {
                    _uiState.value = VoiceUiState.Idle
                }
        }
    }

    override fun onCleared() {
        super.onCleared()
        mediaRecorder?.release()
        mediaPlayer?.release()
        // Clean up any orphaned TTS audio files
        currentTtsFile?.delete()
        audioFile?.delete()
    }
}
