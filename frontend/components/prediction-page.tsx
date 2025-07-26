"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Loader2, Brain, TreePine, Zap, Network, Target, ChevronDown } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface CollapsibleProps {
  title: string
  children: React.ReactNode
  defaultOpen?: boolean
}

function Collapsible({ title, children, defaultOpen = false }: CollapsibleProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen)

  return (
    <div className="border border-border rounded-lg">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-4 py-3 text-left flex items-center justify-between hover:bg-muted/50 transition-colors"
      >
        <span className="font-medium">{title}</span>
        <ChevronDown className={`h-4 w-4 transition-transform ${isOpen ? "rotate-180" : ""}`} />
      </button>
      {isOpen && (
        <div className="px-4 pb-4 border-t border-border">
          {children}
        </div>
      )}
    </div>
  )
}

interface PredictionResult {
  input_data: number[]
  predictions: {
    ann: {
      class_id: number
      class_label: string
      probability: number
    }
    random_forest: {
      class_id: number
      class_label: string
    }
    xgboost: {
      class_id: number
      class_label: string
    }
    knn: {
      class_id: number
      class_label: string
    }
    meta?: {
      class_id: number
      class_label: string
      probability: number
    }
  }
  metadata: {
    timestamp: string
    sensor_names: string[]
    model_versions: {
      ann: string
      random_forest: string
      xgboost: string
      knn: string
    }
  }
}

const sensorLabels = [
  { name: "MQ136", description: "Cảm biến khí đa năng" },
  { name: "MQ137", description: "Cảm biến khí ammonia" },
  { name: "TEMP", description: "Nhiệt độ (°C)" },
  { name: "HUMI", description: "Độ ẩm (%)" },
]

const odorLabels: { [key: string]: string } = {
  "Thịt loại 1": "Thịt loại 1",
  "Thịt loại 2": "Thịt loại 2", 
  "Thịt loại 3": "Thịt loại 3",
  "Thịt loại 4": "Thịt loại 4",
  "Thịt hỏng": "Thịt hỏng",
}

export default function PredictionPage() {
  const [sensorData, setSensorData] = useState<string[]>(Array(4).fill(""))
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleInputChange = (index: number, value: string) => {
    const newData = [...sensorData]
    newData[index] = value
    setSensorData(newData)
  }

  const handlePredict = async () => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      // Validate input
      const numericData = sensorData.map((val) => {
        const num = Number.parseFloat(val)
        if (isNaN(num)) {
          throw new Error(`Giá trị không hợp lệ: ${val}`)
        }
        return num
      })

      // Call API
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sensor_data: numericData,
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Có lỗi xảy ra")
    } finally {
      setIsLoading(false)
    }
  }

  const loadSampleData = () => {
    const sampleData = ["2530", "1075", "25.5", "65.2"]
    setSensorData(sampleData)
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Dự đoán mùi từ dữ liệu cảm biến</CardTitle>
          <CardDescription>Nhập dữ liệu từ 4 cảm biến để dự đoán loại mùi thịt</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {sensorLabels.map((sensor, index) => (
              <div key={sensor.name} className="space-y-2">
                <Label htmlFor={`sensor-${index}`}>{sensor.name}</Label>
                <Input
                  id={`sensor-${index}`}
                  type="number"
                  step="0.1"
                  placeholder="0.0"
                  value={sensorData[index]}
                  onChange={(e) => handleInputChange(index, e.target.value)}
                />
                <p className="text-xs text-muted-foreground">{sensor.description}</p>
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <Button
              onClick={handlePredict}
              disabled={isLoading || sensorData.some((val) => val === "")}
              className="flex-1"
            >
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Dự đoán
            </Button>
            <Button variant="outline" onClick={loadSampleData}>
              Dữ liệu mẫu
            </Button>
          </div>
        </CardContent>
      </Card>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {result && (
        <div className="space-y-6">
          {/* Meta Model Result - Main Result */}
          {result.predictions.meta && (
            <Card className="border-2 border-primary">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="h-5 w-5 mr-2" />
                  Kết quả dự đoán cuối cùng (Meta Model)
                </CardTitle>
                <CardDescription>
                  Kết quả được tối ưu hóa từ 4 mô hình AI cơ sở
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center space-y-4">
                  <div className="text-4xl font-bold text-primary">
                    {odorLabels[result.predictions.meta.class_label]}
                  </div>
                  <div className="text-lg text-muted-foreground">
                    Độ tin cậy: {(result.predictions.meta.probability * 100).toFixed(2)}%
                  </div>
                  <Badge variant="default" className="text-sm px-4 py-2">
                    Meta Model
                  </Badge>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Base Models in Collapsible */}
          <Collapsible title="Chi tiết kết quả từ 4 mô hình cơ sở" defaultOpen={false}>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mt-4">
              <Card>
                <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                  <Brain className="h-4 w-4 mr-2" />
                  <CardTitle className="text-sm font-medium">Neural Network (ANN)</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold">{odorLabels[result.predictions.ann.class_label]}</div>
                  <div className="text-sm text-muted-foreground mt-1">
                    Độ tin cậy: {(result.predictions.ann.probability * 100).toFixed(2)}%
                  </div>
                  <div className="flex items-center space-x-2 mt-2">
                    <Badge variant="outline">{result.metadata.model_versions.ann}</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                  <TreePine className="h-4 w-4 mr-2" />
                  <CardTitle className="text-sm font-medium">Random Forest</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold">{odorLabels[result.predictions.random_forest.class_label]}</div>
                  <div className="flex items-center space-x-2 mt-2">
                    <Badge variant="outline">{result.metadata.model_versions.random_forest}</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                  <Zap className="h-4 w-4 mr-2" />
                  <CardTitle className="text-sm font-medium">XGBoost</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold">{odorLabels[result.predictions.xgboost.class_label]}</div>
                  <div className="flex items-center space-x-2 mt-2">
                    <Badge variant="outline">{result.metadata.model_versions.xgboost}</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                  <Network className="h-4 w-4 mr-2" />
                  <CardTitle className="text-sm font-medium">K-Nearest Neighbors</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold">{odorLabels[result.predictions.knn.class_label]}</div>
                  <div className="flex items-center space-x-2 mt-2">
                    <Badge variant="outline">{result.metadata.model_versions.knn}</Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </Collapsible>
        </div>
      )}

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>Chi tiết kết quả</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <p className="text-sm">
                <strong>Thời gian dự đoán:</strong> {new Date(result.metadata.timestamp).toLocaleString("vi-VN")}
              </p>
              <p className="text-sm">
                <strong>Dữ liệu đầu vào:</strong> [{result.input_data.map(val => val.toFixed(2)).join(", ")}]
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-4">
                {result.metadata.sensor_names.map((sensor, index) => (
                  <div key={sensor} className="text-center p-2 bg-muted rounded">
                    <div className="text-xs text-muted-foreground">{sensor}</div>
                    <div className="font-mono text-sm">{result.input_data[index].toFixed(2)}</div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
