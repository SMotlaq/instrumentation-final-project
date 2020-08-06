/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define led1_Pin GPIO_PIN_13
#define led1_GPIO_Port GPIOC
#define reserved1_Pin GPIO_PIN_4
#define reserved1_GPIO_Port GPIOA
#define wemos_As1_Pin GPIO_PIN_5
#define wemos_As1_GPIO_Port GPIOA
#define reserved2_Pin GPIO_PIN_6
#define reserved2_GPIO_Port GPIOA
#define wemos_As2_Pin GPIO_PIN_7
#define wemos_As2_GPIO_Port GPIOA
#define wemos_R2_Pin GPIO_PIN_4
#define wemos_R2_GPIO_Port GPIOB
#define first_AS_Pin GPIO_PIN_5
#define first_AS_GPIO_Port GPIOB
#define wemos_R1_Pin GPIO_PIN_6
#define wemos_R1_GPIO_Port GPIOB
#define second_AS_Pin GPIO_PIN_7
#define second_AS_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
