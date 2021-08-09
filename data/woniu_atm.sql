/*
 Navicat Premium Data Transfer

 Source Server         : mysql5.7
 Source Server Type    : MySQL
 Source Server Version : 50734
 Source Host           : localhost:3306
 Source Schema         : woniu_atm

 Target Server Type    : MySQL
 Target Server Version : 50734
 File Encoding         : 65001

 Date: 09/08/2021 18:03:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '账户ID',
  `name` varchar(255) NOT NULL COMMENT '账户名',
  `password` varchar(255) NOT NULL COMMENT '账户密码',
  `card_id` varchar(30) NOT NULL COMMENT '卡号',
  `balance` decimal(10,2) NOT NULL DEFAULT '0.01' COMMENT '余额',
  `today_money` decimal(10,0) DEFAULT '0' COMMENT '当日取款最大金额',
  `last_get_money_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_card_id_uindex` (`card_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of account
-- ----------------------------
BEGIN;
INSERT INTO `account` VALUES (1, 'root', '123456', '6223112332423423', 5500.01, 0, NULL);
INSERT INTO `account` VALUES (2, 'zhangsan', '123456', '6223112332423490', 0.00, 0, NULL);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
