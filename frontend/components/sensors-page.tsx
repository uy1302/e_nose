"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2, Thermometer, Droplets, Wind } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import SensorDetailModal from "@/components/sensor-detail-modal"

interface SensorInfo {
  sensor_features: string[]
  sensor_count: number
  sensor_types: {
    gas_sensors: string[]
    environmental_sensors: string[]
  }
  sensor_descriptions: {
    [key: string]: string
  }
}

const sensorIcons: { [key: string]: React.ReactNode } = {
  TEMP: <Thermometer className="h-4 w-4" />,
  HUMI: <Droplets className="h-4 w-4" />,
  MQ136: <Wind className="h-4 w-4" />,
  MQ137: <Wind className="h-4 w-4" />,
}

export default function SensorsPage() {
  const [sensorInfo, setSensorInfo] = useState<SensorInfo | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [selectedSensor, setSelectedSensor] = useState<string | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  useEffect(() => {
    fetchSensorInfo()
  }, [])

  const fetchSensorInfo = async () => {
    try {
      const response = await fetch("/api/sensors")

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setSensorInfo(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Có lỗi xảy ra khi tải thông tin cảm biến")
    } finally {
      setIsLoading(false)
    }
  }

  const handleSensorClick = (sensor: string) => {
    setSelectedSensor(sensor)
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setSelectedSensor(null)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Đang tải thông tin cảm biến...</span>
      </div>
    )
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    )
  }

  if (!sensorInfo) {
    return (
      <Alert>
        <AlertDescription>Không có dữ liệu cảm biến</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Tổng quan hệ thống cảm biến</CardTitle>
          <CardDescription>Thông tin chi tiết về các cảm biến trong hệ thống E-Nose</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">4</div>
              <div className="text-sm text-muted-foreground">Tổng số cảm biến</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">2</div>
              <div className="text-sm text-muted-foreground">Cảm biến khí</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">2</div>
              <div className="text-sm text-muted-foreground">Cảm biến môi trường</div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Wind className="mr-2 h-5 w-5" />
              Cảm biến khí (Gas Sensors)
            </CardTitle>
            <CardDescription>Các cảm biến phát hiện khí và hóa chất trong không khí</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {sensorInfo.sensor_types.gas_sensors.map((sensor) => (
              <div 
                key={sensor} 
                className="flex items-center justify-between p-3 border rounded-lg hover:shadow-md transition-all duration-200 cursor-pointer hover:scale-[1.02] hover:bg-muted/50"
                onClick={() => handleSensorClick(sensor)}
              >
                <div className="flex items-center space-x-3">
                  {sensorIcons[sensor]}
                  <div>
                    <div className="font-medium">{sensor}</div>
                    <div className="text-sm text-muted-foreground">{sensorInfo.sensor_descriptions[sensor]}</div>
                  </div>
                </div>
                <Badge variant="secondary">Gas</Badge>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Thermometer className="mr-2 h-5 w-5" />
              Cảm biến môi trường
            </CardTitle>
            <CardDescription>Các cảm biến đo điều kiện môi trường xung quanh</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {sensorInfo.sensor_types.environmental_sensors.map((sensor) => (
              <div 
                key={sensor} 
                className="flex items-center justify-between p-3 border rounded-lg hover:shadow-md transition-all duration-200 cursor-pointer hover:scale-[1.02] hover:bg-muted/50"
                onClick={() => handleSensorClick(sensor)}
              >
                <div className="flex items-center space-x-3">
                  {sensorIcons[sensor]}
                  <div>
                    <div className="font-medium">{sensor}</div>
                    <div className="text-sm text-muted-foreground">{sensorInfo.sensor_descriptions[sensor]}</div>
                  </div>
                </div>
                <Badge variant="outline">Environment</Badge>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>



      {/* Sensor Detail Modal */}
      {selectedSensor && sensorInfo && (
        <SensorDetailModal
          isOpen={isModalOpen}
          onClose={handleCloseModal}
          sensor={selectedSensor}
          sensorInfo={sensorInfo}
        />
      )}
    </div>
  )
}
