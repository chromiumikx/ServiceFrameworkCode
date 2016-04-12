#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;

int16_t a[3];
int16_t g[3];

bool blinkState = false;

void setup() {
    Wire.begin();
    Serial.begin(9600);

    mpu.initialize();
    //TODO：或需将灵敏度设置为4g
}

void loop() {
	
  mpu.getMotion6(&a[0],&a[1],&a[2],&g[0],&g[1],&g[2]);
	
	//发送十六进制数字（或字符），不直接发送数字的字符
	for(i=0;i<=2;i++){
    //TODO：此处更改后未烧录
		a[i]=a[i]/167;//除1672是真实加速度，作10倍处理
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
    g[i]=g[i]/131;//真实（整数值）角速度
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