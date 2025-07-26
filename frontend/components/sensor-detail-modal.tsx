"use client"

import React from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogClose } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Thermometer, Droplets, Wind, Gauge, Zap, Activity } from "lucide-react"

interface SensorDetail {
  fullName: string
  detectedGases?: string[]
  detectedParameters?: string[]
  workingVoltage?: string
  heatingVoltage?: string
  loadResistance?: string
  heatingResistance?: string
  sensingResistance?: string
  range?: string
  detectionRange?: string
  measurementRange?: string
  accuracy?: string
  operatingTemp?: string
  operatingHumidity?: string
  responseTime?: string
  recoveryTime?: string
  preheatingTime?: string
  resolution?: string
  samplingRate?: string
  description?: string
  applications?: string[]
  characteristics?: string[]
  specifications?: { [key: string]: string }
  color?: string
}

const sensorIcons: { [key: string]: React.ReactNode } = {
  TEMP: <Thermometer className="h-6 w-6" />,
  HUMI: <Droplets className="h-6 w-6" />,
  MQ2: <Wind className="h-6 w-6" />,
  MQ3: <Wind className="h-6 w-6" />,
  MQ4: <Wind className="h-6 w-6" />,
  MQ6: <Wind className="h-6 w-6" />,
  MQ7: <Wind className="h-6 w-6" />,
  MQ135: <Wind className="h-6 w-6" />,
}

const getSensorDetails = (sensor: string): SensorDetail => {
  const details: { [key: string]: SensorDetail } = {
    MQ2: {
      fullName: "Cảm biến khí MQ-2",
      detectedGases: ["LPG", "Propane", "Methane", "Alcohol", "Hydrogen", "Smoke"],
      workingVoltage: "5V",
      heatingVoltage: "5V ± 0.1V",
      loadResistance: "20kΩ",
      heatingResistance: "33Ω ± 5%",
      detectionRange: "300-10000ppm",
      preheatingTime: "20s",
      responseTime: "< 10s",
      recoveryTime: "< 30s",
      applications: ["Phát hiện rò rỉ khí", "Hệ thống báo khói", "Thiết bị an toàn công nghiệp"],
      color: "text-red-600"
    },
    MQ3: {
      fullName: "Cảm biến khí MQ-3",
      detectedGases: ["Alcohol", "Ethanol", "Benzine"],
      workingVoltage: "5V",
      heatingVoltage: "5V ± 0.1V",
      loadResistance: "200kΩ",
      heatingResistance: "33Ω ± 5%",
      detectionRange: "0.05-10mg/L",
      preheatingTime: "20s",
      responseTime: "< 10s",
      recoveryTime: "< 30s",
      applications: ["Máy đo nồng độ cồn", "Hệ thống kiểm soát xe", "Thiết bị y tế"],
      color: "text-blue-600"
    },
    MQ4: {
      fullName: "Cảm biến khí MQ-4",
      detectedGases: ["Methane", "CNG Gas"],
      workingVoltage: "5V",
      heatingVoltage: "5V ± 0.1V",
      loadResistance: "20kΩ",
      heatingResistance: "33Ω ± 5%",
      detectionRange: "200-10000ppm",
      preheatingTime: "20s",
      responseTime: "< 10s",
      recoveryTime: "< 30s",
      applications: ["Phát hiện rò rỉ khí tự nhiên", "Hệ thống an toàn gia đình", "Công nghiệp dầu khí"],
      color: "text-green-600"
    },
    MQ6: {
      fullName: "Cảm biến khí MQ-6",
      detectedGases: ["LPG", "Butane", "Propane"],
      workingVoltage: "5V",
      heatingVoltage: "5V ± 0.1V",
      loadResistance: "20kΩ",
      heatingResistance: "33Ω ± 5%",
      detectionRange: "200-10000ppm",
      preheatingTime: "20s",
      responseTime: "< 10s",
      recoveryTime: "< 30s",
      applications: ["Phát hiện rò rỉ gas LPG", "Hệ thống báo động", "Thiết bị an toàn bếp gas"],
      color: "text-orange-600"
    },
    MQ7: {
      fullName: "Cảm biến khí MQ-7",
      detectedGases: ["Carbon Monoxide (CO)"],
      workingVoltage: "5V",
      heatingVoltage: "5V ± 0.1V",
      loadResistance: "10kΩ",
      heatingResistance: "33Ω ± 5%",
      detectionRange: "20-2000ppm",
      preheatingTime: "48h",
      responseTime: "< 10s",
      recoveryTime: "< 30s",
      applications: ["Phát hiện khí CO", "Hệ thống báo động độc hại", "An toàn lao động"],
      color: "text-purple-600"
    },
    MQ135: {
      fullName: "Cảm biến chất lượng không khí MQ-135",
      detectedGases: ["NH3", "NOx", "Alcohol", "Benzene", "CO2", "Smoke"],
      workingVoltage: "5V",
      heatingVoltage: "5V ± 0.1V",
      loadResistance: "20kΩ",
      heatingResistance: "33Ω ± 5%",
      detectionRange: "10-300ppm (NH3), 10-1000ppm (Benzene)",
      preheatingTime: "20s",
      responseTime: "< 10s",
      recoveryTime: "< 30s",
      applications: ["Giám sát chất lượng không khí", "Hệ thống thông gió thông minh", "IoT môi trường"],
      color: "text-indigo-600"
    },
    TEMP: {
      fullName: "Cảm biến nhiệt độ DHT22",
      detectedParameters: ["Temperature"],
      workingVoltage: "3.3V - 5V",
      accuracy: "±0.5°C",
      resolution: "0.1°C",
      measurementRange: "-40°C to +80°C",
      responseTime: "2s",
      samplingRate: "0.5Hz",
      applications: ["Giám sát môi trường", "Hệ thống HVAC", "Điều khiển tự động"],
      color: "text-red-500"
    },
    HUMI: {
      fullName: "Cảm biến độ ẩm DHT22",
      detectedParameters: ["Humidity"],
      workingVoltage: "3.3V - 5V",
      accuracy: "±2-5% RH",
      resolution: "0.1% RH",
      measurementRange: "0-100% RH",
      responseTime: "2s",
      samplingRate: "0.5Hz",
      applications: ["Giám sát độ ẩm", "Hệ thống tưới tiêu", "Kho bảo quản"],
      color: "text-blue-500"
    }
  }
  
  return details[sensor] || {}
}

export default function SensorDetailModal({ isOpen, onClose, sensor, sensorInfo }: {
  isOpen: boolean
  onClose: () => void
  sensor: string
  sensorInfo: {
    sensor_descriptions: { [key: string]: string }
    sensor_types: {
      gas_sensors: string[]
      environmental_sensors: string[]
    }
  }
}) {
  const sensorDetail = getSensorDetails(sensor)
  const isGasSensor = sensorInfo.sensor_types.gas_sensors.includes(sensor)

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogClose onClose={onClose} />
        
        <DialogHeader className="pb-4">
          <DialogTitle className="flex items-center space-x-3 text-xl">
            <div className={`${sensorDetail.color} bg-gradient-to-br from-background to-muted p-3 rounded-full`}>
              {sensorIcons[sensor]}
            </div>
            <div>
              <div className="font-bold">{sensor}</div>
              <div className="text-sm text-muted-foreground font-normal">{sensorDetail.fullName}</div>
            </div>
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          {/* Description */}
          <Card className="card-hover-glow">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Activity className="h-5 w-5" />
                <span>Mô tả chức năng</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm">{sensorInfo.sensor_descriptions[sensor]}</p>
              <div className="mt-3 flex space-x-2">
                <Badge variant={isGasSensor ? "default" : "outline"}>
                  {isGasSensor ? "Gas Sensor" : "Environmental Sensor"}
                </Badge>
                {sensorDetail.detectedGases && (
                  <Badge variant="secondary">
                    {sensorDetail.detectedGases.length} loại khí
                  </Badge>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Technical Specifications */}
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="card-hover-glow">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Gauge className="h-5 w-5" />
                  <span>Thông số kỹ thuật</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {sensorDetail.workingVoltage && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Điện áp hoạt động:</span>
                    <span className="text-sm font-medium">{sensorDetail.workingVoltage}</span>
                  </div>
                )}
                {sensorDetail.accuracy && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Độ chính xác:</span>
                    <span className="text-sm font-medium">{sensorDetail.accuracy}</span>
                  </div>
                )}
                {sensorDetail.detectionRange && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Phạm vi đo:</span>
                    <span className="text-sm font-medium">{sensorDetail.detectionRange}</span>
                  </div>
                )}
                {sensorDetail.responseTime && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Thời gian phản hồi:</span>
                    <span className="text-sm font-medium">{sensorDetail.responseTime}</span>
                  </div>
                )}
                {sensorDetail.loadResistance && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Điện trở tải:</span>
                    <span className="text-sm font-medium">{sensorDetail.loadResistance}</span>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="card-hover-glow">
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  <Zap className="h-5 w-5" />
                  <span>Hiệu suất</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {sensorDetail.preheatingTime && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Thời gian làm nóng:</span>
                    <span className="text-sm font-medium">{sensorDetail.preheatingTime}</span>
                  </div>
                )}
                {sensorDetail.recoveryTime && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Thời gian phục hồi:</span>
                    <span className="text-sm font-medium">{sensorDetail.recoveryTime}</span>
                  </div>
                )}
                {sensorDetail.samplingRate && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Tần số lấy mẫu:</span>
                    <span className="text-sm font-medium">{sensorDetail.samplingRate}</span>
                  </div>
                )}
                {sensorDetail.resolution && (
                  <div className="flex justify-between">
                    <span className="text-sm text-muted-foreground">Độ phân giải:</span>
                    <span className="text-sm font-medium">{sensorDetail.resolution}</span>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Detected Gases/Parameters */}
          {(sensorDetail.detectedGases || sensorDetail.detectedParameters) && (
            <Card className="card-hover-glow">
              <CardHeader>
                <CardTitle>
                  {isGasSensor ? "Khí có thể phát hiện" : "Tham số đo lường"}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {(sensorDetail.detectedGases || sensorDetail.detectedParameters || []).map((item: string, index: number) => (
                    <Badge key={index} variant="outline" className="text-xs">
                      {item}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Applications */}
          {sensorDetail.applications && (
            <Card className="card-hover-glow">
              <CardHeader>
                <CardTitle>Ứng dụng thực tế</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {sensorDetail.applications.map((app: string, index: number) => (
                    <li key={index} className="flex items-start space-x-2">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                      <span className="text-sm">{app}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
} 