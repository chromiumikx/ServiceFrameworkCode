#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;

int i;
int16_t a[3];
int16_t g[3];
uint8_t range_a=1;//设置加速度计读数范围——+-4g
uint8_t range_g=1;//设置陀螺仪读数范围——+-500 degree/s

bool blinkState = false;

void setup() {
    Wire.begin();
    Serial.begin(9600);

    mpu.initialize();
    mpu.setFullScaleAccelRange(range_a);
    mpu.setFullScaleGyroRange(range_g);
}

void loop() {
	
  mpu.getMotion6(&a[0],&a[1],&a[2],&g[0],&g[1],&g[2]);
	
	//发送十六进制数字（或字符），不直接发送数字的字符
	for(i=0;i<=2;i++){
    //TODO：此处更改后未烧录
		a[i]=a[i]/83.6;//动态范围+-4g，所读数除836得真实加速度，再作10倍处理
		if(a[i]<0){
			//以1000+的数表示负数，降低编码和解码处理时间
			a[i]=1000-a[i];
		}
    else{
      a[i]=a[i]+2000;
    }
    Serial.print(" ");
    Serial.print(a[i]);
	}
  for(i=0;i<=2;i++){
    g[i]=g[i]/65.5;//动态范围是+-500 degree/s，所读数除65.5得真实（整数值）角速度
    if(g[i]<0){
      g[i]=1000-g[i];
    }
    else{
      g[i]=g[i]+2000;
    }
    Serial.print(" ");
    Serial.print(g[i]);
  } 
  Serial.print(" ");
  Serial.print("h");//仍以“h”作为帧的分界

  blinkState = !blinkState;
}
