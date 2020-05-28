/*
 * Copyright 2017 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.example.trash_recognizer

import android.Manifest
import android.app.AlertDialog
import android.content.Context
import android.content.pm.PackageManager
import android.content.res.Configuration
import android.graphics.*
import android.hardware.camera2.*
import android.media.Image
import android.media.ImageReader
import android.os.Bundle
import android.os.Handler
import android.os.HandlerThread
import android.os.Trace
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import android.util.Log
import android.util.Size
import android.util.SparseIntArray
import android.view.*
import android.widget.TextView
import androidx.fragment.app.Fragment
import com.example.trash_recognizer.Classifier
import com.example.trash_recognizer.ImageUtils
import java.io.File
import java.nio.ByteBuffer
import java.util.*
import java.util.concurrent.Semaphore
import java.util.concurrent.TimeUnit
import kotlin.collections.ArrayList

class Camera2BasicFragment : Fragment(),
        ActivityCompat.OnRequestPermissionsResultCallback {

    private var rgbBytes: IntArray? = null
    private lateinit var previewReader: ImageReader
    private val mInputSize = 224
    private val mModelPath = "model.tflite"
    private val mLabelPath = "label.txt"
    private var rgbFrameBitmap: Bitmap? = null
    private val yuvBytes = arrayOfNulls<ByteArray>(3)
    private lateinit var previewSize: Size

    public val onImageAvailableListener = ImageReader.OnImageAvailableListener {


        val image: Image = it.acquireLatestImage()
        val planes = image.getPlanes()

        val yRowStride = planes[0].getRowStride()
        val uvRowStride = planes[1].getRowStride()
        val uvPixelStride = planes[1].getRowStride()

        val imageConverter = ImageUtils.convertYUV420ToARGB8888(yuvBytes[0],yuvBytes[1],yuvBytes[2], previewSize.width, previewSize.height, yRowStride,uvRowStride,uvPixelStride, rgbBytes)

    }
    protected fun fillBytes(planes: Array<Image.Plane>, yuvBytes: Array<ByteArray?>) {
        for (i in planes.indices) {
            val buffer = planes[i].buffer
            if (yuvBytes[i] == null) {
                yuvBytes[i] = ByteArray(buffer.capacity())
            }
            buffer.get(yuvBytes[i])
        }
    }
    public fun addPixelValue(byteBuffer: ByteBuffer, intValue: Int): ByteBuffer {

        byteBuffer.put((intValue.shr(16) and 0xFF).toByte())
        byteBuffer.put((intValue.shr(8) and 0xFF).toByte())
        byteBuffer.put((intValue and 0xFF).toByte())
        return byteBuffer
    }



}
