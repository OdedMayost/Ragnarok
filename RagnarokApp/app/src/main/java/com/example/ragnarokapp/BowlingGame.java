package com.example.ragnarokapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.Window;
import android.widget.ImageButton;

public class BowlingGame extends AppCompatActivity {

    private SensorManager sensorManager;
    private float accelerometer[] = new float[2];

    private static final String TAG = "ICT";
    String IP;
    Integer Port = 50000;
    Handler message_handler;
    String data_message;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        getSupportActionBar().hide();
        setContentView(R.layout.activity_bowling_game);

        Intent bowling_game = getIntent();
        IP = bowling_game.getStringExtra("IP");
        Log.d(TAG, "IP = " + IP);

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        Sensor sensor = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        sensorManager.registerListener(listener, sensor, SensorManager.SENSOR_DELAY_NORMAL);

        ImageButton button = (ImageButton) findViewById(R.id.acceleration_button);
        button.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                float this_accelerometer = 0;
                if (event.getAction() == MotionEvent.ACTION_DOWN) {
                    this_accelerometer = accelerometer[0];
                } else if (event.getAction() == MotionEvent.ACTION_UP) {
                    this_accelerometer = accelerometer[0] - this_accelerometer;
                    String data = "ACLRT~" + String.valueOf(this_accelerometer) + "~" + String.valueOf(accelerometer[1]);
                    send_message(data);
                }
                return true;
            }
        });

        message_handler = new Handler(Looper.getMainLooper()) {
            @Override
            public void handleMessage(Message message) {
                String receive = (String) message.obj;
                if (receive.length() >= 5){
                    data_message = receive.substring(5);
                    if (data_message.equals("ENDED")){
                        Intent homepage = new Intent(getApplicationContext(), HomepageActivity.class);
                        homepage.putExtra("IP", IP);
                        startActivity(homepage);
                    }
                }
                Log.d(TAG, "Information received = " + data_message);
            }
        };
    }

    public void send_message(String data) {
        TcpBySize bg = new TcpBySize(this.message_handler, this.IP, this.Port);
        bg.execute(data);
    }

    public void arrow_right(View view){
        String message = "PMOVE~1";
        send_message(message);
        Log.e(TAG, "move right");
    }

    public void arrow_left(View view){
        String message = "PMOVE~2";
        send_message(message);
        Log.e(TAG, "move left");
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (sensorManager != null) {
            sensorManager.unregisterListener(listener);
        }
    }

    private SensorEventListener listener = new SensorEventListener() {
        @Override
        public void onSensorChanged(SensorEvent event) {
            float xValue = Math.abs(event.values[0]);
            float yValue = Math.abs(event.values[1]);
            float zValue = Math.abs(event.values[2]);
            accelerometer[0] = (float) Math.sqrt(Math.pow(xValue, 2) + Math.pow(yValue, 2) + Math.pow(zValue, 2));
            accelerometer[1] = direction_injury(xValue, yValue);
        }

        @Override
        public void onAccuracyChanged(Sensor sensor, int accuracy) {
        }
    };

    public float direction_injury(float xValue, float yValue) {
        double direction = (double) yValue / xValue;
        direction = Math.atan(direction);
        direction = Math.toDegrees(direction);
        return (float) direction;
    }

}