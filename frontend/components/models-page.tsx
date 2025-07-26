"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2, Brain, TreePine, Zap, Target, Network } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface ModelInfo {
  models: {
    [key: string]: {
      name: string
      type: string
      accuracy: string
      description: string
    }
  }
  classes: string[]
  ensemble_method: string
}

const modelIcons: { [key: string]: React.ReactNode } = {
  ann: <Brain className="h-5 w-5" />,
  random_forest: <TreePine className="h-5 w-5" />,
  xgboost: <Zap className="h-5 w-5" />,
  knn: <Network className="h-5 w-5" />,
  meta: <Target className="h-5 w-5" />,
}

const odorLabels: { [key: string]: string } = {
  "Thịt loại 1": "Thịt loại 1",
  "Thịt loại 2": "Thịt loại 2", 
  "Thịt loại 3": "Thịt loại 3",
  "Thịt loại 4": "Thịt loại 4",
  "Thịt hỏng": "Thịt hỏng",
}

const typeColors: { [key: string]: string } = {
  deep_learning: "bg-blue-100 text-blue-800",
  ensemble: "bg-green-100 text-green-800",
  gradient_boosting: "bg-purple-100 text-purple-800",
  instance_based: "bg-orange-100 text-orange-800",
  meta_learning: "bg-red-100 text-red-800",
}

export default function ModelsPage() {
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchModelInfo()
  }, [])

  const fetchModelInfo = async () => {
    try {
      const response = await fetch("/api/models")

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setModelInfo(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Có lỗi xảy ra khi tải thông tin mô hình")
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">Đang tải thông tin mô hình...</span>
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

  if (!modelInfo) {
    return (
      <Alert>
        <AlertDescription>Không có dữ liệu mô hình</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Tổng quan hệ thống AI</CardTitle>
          <CardDescription>
            Thông tin về các mô hình trí tuệ nhân tạo được sử dụng trong hệ thống E-Nose
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">5</div>
              <div className="text-sm text-muted-foreground">Mô hình AI</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">{modelInfo.classes.length}</div>
              <div className="text-sm text-muted-foreground">Loại mùi</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">97.61%</div>
              <div className="text-sm text-muted-foreground">Độ chính xác Meta Model</div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-1 lg:grid-cols-3">
        {Object.entries(modelInfo.models).map(([key, model]) => (
          <Card key={key} className="h-full">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                {modelIcons[key]}
                <span>{model.name}</span>
              </CardTitle>
              <CardDescription>{model.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Loại mô hình:</span>
                <Badge className={typeColors[model.type] || "bg-gray-100 text-gray-800"}>
                  {model.type.replace("_", " ").toUpperCase()}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Độ chính xác:</span>
                <Badge variant="secondary">{model.accuracy}</Badge>
              </div>
              <div className="pt-2 border-t">
                <p className="text-xs text-muted-foreground">{model.description}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Target className="mr-2 h-5 w-5" />
              Các loại mùi có thể phát hiện
            </CardTitle>
            <CardDescription>Danh sách các loại mùi mà hệ thống có thể nhận diện</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-3 md:grid-cols-2">
              {modelInfo.classes.map((odorClass, index) => (
                <div key={odorClass} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium">{odorLabels[odorClass] || odorClass}</div>
                    <div className="text-sm text-muted-foreground">Class ID: {index}</div>
                  </div>
                  <Badge variant="outline">{odorClass}</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Phương pháp kết hợp</CardTitle>
            <CardDescription>Cách thức kết hợp kết quả từ các mô hình khác nhau</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 bg-muted rounded-lg">
              <div className="font-medium mb-2">Meta Learning</div>
              <Badge variant="secondary" className="mb-2">
                LINEAR REGRESSION
              </Badge>
              <p className="text-sm text-muted-foreground">
                Hệ thống sử dụng Meta Model để kết hợp kết quả từ 4 mô hình AI cơ sở,
                đạt được độ chính xác cao nhất 97.61% trên tập dữ liệu test.
              </p>
            </div>

            <div className="space-y-2">
              <h4 className="font-medium">Quy trình dự đoán:</h4>
              <ol className="text-sm text-muted-foreground space-y-1 list-decimal list-inside">
                <li>Dữ liệu 4 cảm biến được chuẩn hóa</li>
                <li>4 mô hình cơ sở (ANN, RF, XGBoost, KNN) thực hiện dự đoán</li>
                <li>Meta Model sử dụng Linear Regression để kết hợp kết quả</li>
                <li>Trả về kết quả cuối cùng với độ tin cậy cao</li>
              </ol>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>So sánh hiệu suất mô hình</CardTitle>
          <CardDescription>Đánh giá và so sánh các mô hình AI trong hệ thống</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Mô hình</th>
                  <th className="text-left p-2">Loại</th>
                  <th className="text-left p-2">Độ chính xác</th>
                  <th className="text-left p-2">Ưu điểm</th>
                  <th className="text-left p-2">Đặc điểm</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(modelInfo.models).map(([key, model]) => (
                  <tr key={key} className="border-b">
                    <td className="p-2">
                      <div className="flex items-center space-x-2">
                        {modelIcons[key]}
                        <span className="font-medium">{model.name}</span>
                      </div>
                    </td>
                    <td className="p-2">
                      <Badge className={typeColors[model.type] || "bg-gray-100 text-gray-800"}>
                        {model.type.replace("_", " ")}
                      </Badge>
                    </td>
                    <td className="p-2">
                      <Badge variant="secondary">{model.accuracy}</Badge>
                    </td>
                    <td className="p-2 text-muted-foreground">
                      {key === "ann" && "Học sâu, xử lý phi tuyến"}
                      {key === "random_forest" && "Ổn định, chống overfitting"}
                      {key === "xgboost" && "Tốc độ cao, hiệu quả"}
                      {key === "knn" && "Đơn giản, hiệu quả"}
                      {key === "meta" && "Kết hợp tối ưu, độ chính xác cao nhất"}
                    </td>
                    <td className="p-2 text-muted-foreground">
                      {key === "ann" && "Neural Network với regularization"}
                      {key === "random_forest" && "Ensemble của decision trees"}
                      {key === "xgboost" && "Gradient boosting tối ưu"}
                      {key === "knn" && "Dựa trên khoảng cách láng giềng"}
                      {key === "meta" && "Linear Regression trên meta-features"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
