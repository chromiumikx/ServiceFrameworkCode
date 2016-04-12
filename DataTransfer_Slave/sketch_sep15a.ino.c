#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"

MPU6050 mpu;

int16_t ax, ay, az;
//int16_t g[3];

bool blinkState = false;

void setup() {
    Wire.begin();
    Serial.begin(9600);

    mpu.initialize();
}

void loop() {
	
	//最好采用getMotion6();
	
	//getRotation(&g[0],&g[1],&g[2]);
	//发送十六进制数字（字符），不直接发送数字的字符
	// for(i=0;i<=2;i++){
		// g[i]=g[i]/131;
		// if(g[i]<0){
			// 以5000+的数表示负数，降低编码和解码处理时间
			// g[i]=g[i]+5000
		// }
		// Serial.print(g[i],HEX);//注意：最好所有数据一次依次处理好，然后一次依次发出去
	// }
	

	
	
	
    mpu.getAcceleration(&ax,&ay,&az);

    //注意：所读数于实际加速度的转换（是否需要？）
	//注意：将实际加速度乘以10，总结果如下：

    ax = ax/836;
    ay = ay/836;
    az = az/836;
    
    Serial.print("h");
    if(ax >= 0 && ax < 10)
    {
      Serial.print("00");
      Serial.print(ax);
    }
    else if(ax > 9 && ax < 100)
    {
      Serial.print("0");
      Serial.print(ax);
    }
    else if(ax > -100 && ax <= -10)
    {
      Serial.print(ax);
    }
    else if(ax > -10 && ax < 0)
    {
      Serial.print("0");
      Serial.print(ax);
    }
    
    if(ay >= 0 && ay < 10)
    {
      Serial.print("00");
      Serial.print(ay);
    }
    else if(ay > 9 && ay < 100)
    {
      Serial.print("0");
      Serial.print(ay);
    }
    else if(ay > -100 && ay <= -10)
    {
      Serial.print(ay);
    }
    else if(ay > -10 && ay < 0)
    {
      Serial.print("0");
      Serial.print(ay);
    }
    
    if(az >= 0 && az < 10)
    {
      Serial.print("00");
      Serial.print(az);
    }
    else if(az > 9 && az < 100)
    {
      Serial.print("0");
      Serial.print(az);
    }
    else if(az > -100 && az <= -10)
    {
      Serial.print(az);
    }
    else if(az > -10 && az < 0)
    {
      Serial.print("0");
      Serial.print(az);
    }
    
    blinkState = !blinkState;
}



