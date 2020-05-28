package com.example.trash_recognizer;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Camera;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;
import android.media.Image;
import android.media.ImageReader;
import kotlin.collections.*;
import kotlin.jvm.JvmDefault;

import com.example.trash_recognizer.Camera2BasicFragment;


import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.sql.Time;
import java.text.SimpleDateFormat;
import java.util.Date;


public class MainActivity extends AppCompatActivity implements SurfaceHolder.Callback {

    private Button button;
    private SurfaceView surfaceView;
    private Camera camera;
    private SurfaceHolder surfaceHolder;
    private android.hardware.Camera.PictureCallback pictureCallback;
    private int INPUT_SIZE=224;
    private int PIXEL_SIZE =3;
    private  int intValue = INPUT_SIZE*INPUT_SIZE;
    public Camera2BasicFragment camera2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.CAMERA}, 100);
            if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                Intent intent = getIntent();
//                finish();
                startActivity(intent);
            }
        }else if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 100);
            if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                Intent intent = getIntent();
                startActivity(intent);
//                finish();

            }
        }else{
            super.onCreate(savedInstanceState);
            setContentView(R.layout.activity_main);

            surfaceView = findViewById(R.id.surfaceView);
            button = findViewById(R.id.button);

            surfaceHolder = surfaceView.getHolder();
            surfaceHolder.addCallback(this);
            surfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);

            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    camera.takePicture(null, null, pictureCallback);
                }
            });

            pictureCallback = new android.hardware.Camera.PictureCallback() {
                @Override
                public void onPictureTaken(byte[] bytes, android.hardware.Camera camera) {
                    camera2.getOnImageAvailableListener();

                    Bitmap bmp = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                    Bitmap cbmp = Bitmap.createBitmap(bmp, 0, 0, bmp.getWidth(), bmp.getHeight(), null, true);

                    cbmp.createScaledBitmap(cbmp, INPUT_SIZE,INPUT_SIZE, false);
                    ByteBuffer byteBuffer = ByteBuffer.allocateDirect(INPUT_SIZE*INPUT_SIZE*PIXEL_SIZE);
                    byteBuffer.order(ByteOrder.nativeOrder());
                    ByteBuffer convertedBytes = camera2.addPixelValue(byteBuffer,intValue);



                    Toast.makeText(getApplicationContext(), "Done!", Toast.LENGTH_LONG).show();

                    MainActivity.this.camera.startPreview();
                }
            };
        }
    }

    private void storePhotoToStorage(Bitmap cbmp, String pathFileName) {
        File outputFile = new File(Environment.getExternalStorageDirectory(), "/DCIM/Camera/IMG_"+pathFileName+".jpg");

        try {
            FileOutputStream fileOutputStream = new FileOutputStream(outputFile);
            cbmp.compress(Bitmap.CompressFormat.JPEG, 100, fileOutputStream);
            fileOutputStream.flush();
            fileOutputStream.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private String currentDateFormat() {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMdd_HH_mm_ss");
        String currentTime = dateFormat.format(new Date());
        return  currentTime;
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        try {
            camera = Camera.open();
        } catch (Exception e) {

        }

        Camera.Parameters parameters;
        parameters = camera.getParameters();
        parameters.setPreviewFrameRate(30);
        parameters.setPreviewSize(352, 288);
        camera.setParameters(parameters);
        camera.setDisplayOrientation(90);
        try {
            camera.setPreviewDisplay(surfaceHolder);
            camera.startPreview();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    @Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
        camera.stopPreview();
        camera.release();
        camera = null;
    }



}
