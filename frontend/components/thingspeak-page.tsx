"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Loader2, Cloud, RefreshCw } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface ThingSpeakData {
  channel_id: string
  name: string
  description: string
  field1: string
  field2: string
  field3: string
  field4: string
  field5: string
  field6: string
  field7: string
  field8: string
  created_at: string
  updated_at: string
  last_entry_id: number
}

interface ThingSpeakPrediction {
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
  }
  thingspeak_data?: ThingSpeakData  // Optional for backward compatibility
  metadata: {
    timestamp: string
    sensor_names: string[]
    thingspeak?: {
      records_fetched: number
      latest_entry_time: string
      api_key: string
    }
  }
}

const odorLabels: { [key: string]: string } = {
  fish_sauce: "Nước mắm",
  garlic: "Tỏi",
  lemon: "Chanh",
  milk: "Sữa",
}

export default function ThingSpeakPage() {
  const [apiKey, setApiKey] = useState("RJNVLFM0O88JP765")
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<ThingSpeakPrediction | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handlePredict = async () => {
    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch("/api/predict/thingspeak", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          api_key: apiKey,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Unknown error' }))
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Có lỗi xảy ra khi kết nối ThingSpeak")
    } finally {
      setIsLoading(false)
    }
  }

  // Helper to get ThingSpeak info from either structure
  const getThingSpeakInfo = () => {
    if (!result) return null
    
    // New structure: metadata.thingspeak
    if (result.metadata?.thingspeak) {
      return {
        api_key: result.metadata.thingspeak.api_key,
        records_fetched: result.metadata.thingspeak.records_fetched,
        latest_entry_time: result.metadata.thingspeak.latest_entry_time,
      }
    }
    
    // Old structure: thingspeak_data
    if (result.thingspeak_data) {
      return {
        channel_id: result.thingspeak_data.channel_id,
        name: result.thingspeak_data.name,
        description: result.thingspeak_data.description,
        updated_at: result.thingspeak_data.updated_at,
        last_entry_id: result.thingspeak_data.last_entry_id,
      }
    }
    
    return null
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Cloud className="mr-2 h-5 w-5" />
            Dự đoán từ ThingSpeak
          </CardTitle>
          <CardDescription>Lấy dữ liệu cảm biến từ ThingSpeak và thực hiện dự đoán</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="api-key">ThingSpeak API Key</Label>
            <Input
              id="api-key"
              type="text"
              placeholder="Nhập API Key của ThingSpeak"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <p className="text-xs text-muted-foreground">API Key để truy cập dữ liệu từ ThingSpeak channel</p>
          </div>

          <Button onClick={handlePredict} disabled={isLoading || !apiKey.trim()} className="w-full">
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Đang lấy dữ liệu...
              </>
            ) : (
              <>
                <RefreshCw className="mr-2 h-4 w-4" />
                Lấy dữ liệu và dự đoán
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {result && (
        <>
          {/* ThingSpeak Info Card - Only show if we have data */}
          {getThingSpeakInfo() && (
            <Card>
              <CardHeader>
                <CardTitle>Thông tin ThingSpeak</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="grid gap-2 md:grid-cols-2">
                  {getThingSpeakInfo()?.channel_id && (
                    <div>
                      <p className="text-sm font-medium">Channel ID:</p>
                      <p className="text-sm text-muted-foreground">{getThingSpeakInfo()?.channel_id}</p>
                    </div>
                  )}
                  {getThingSpeakInfo()?.name && (
                    <div>
                      <p className="text-sm font-medium">Tên Channel:</p>
                      <p className="text-sm text-muted-foreground">{getThingSpeakInfo()?.name}</p>
                    </div>
                  )}
                  {getThingSpeakInfo()?.api_key && (
                    <div>
                      <p className="text-sm font-medium">API Key:</p>
                      <p className="text-sm text-muted-foreground font-mono">{getThingSpeakInfo()?.api_key}</p>
                    </div>
                  )}
                  {getThingSpeakInfo()?.records_fetched && (
                    <div>
                      <p className="text-sm font-medium">Records lấy được:</p>
                      <p className="text-sm text-muted-foreground">{getThingSpeakInfo()?.records_fetched}</p>
                    </div>
                  )}
                  {(getThingSpeakInfo()?.updated_at || getThingSpeakInfo()?.latest_entry_time) && (
                    <div>
                      <p className="text-sm font-medium">Cập nhật lần cuối:</p>
                      <p className="text-sm text-muted-foreground">
                        {new Date(getThingSpeakInfo()?.updated_at || getThingSpeakInfo()?.latest_entry_time || '').toLocaleString("vi-VN")}
                      </p>
                    </div>
                  )}
                  {getThingSpeakInfo()?.last_entry_id && (
                    <div>
                      <p className="text-sm font-medium">Entry ID:</p>
                      <p className="text-sm text-muted-foreground">{getThingSpeakInfo()?.last_entry_id}</p>
                    </div>
                  )}
                </div>
                {getThingSpeakInfo()?.description && (
                  <div>
                    <p className="text-sm font-medium">Mô tả:</p>
                    <p className="text-sm text-muted-foreground">{getThingSpeakInfo()?.description}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Prediction Results */}
          <div className="grid gap-4 md:grid-cols-3">
            <Card>
              <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Neural Network (ANN)</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{odorLabels[result.predictions.ann.class_label] || result.predictions.ann.class_label}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Random Forest</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{odorLabels[result.predictions.random_forest.class_label] || result.predictions.random_forest.class_label}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">XGBoost</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{odorLabels[result.predictions.xgboost.class_label] || result.predictions.xgboost.class_label}</div>
              </CardContent>
            </Card>
          </div>

          {/* Sensor Data */}
          <Card>
            <CardHeader>
              <CardTitle>Dữ liệu cảm biến từ ThingSpeak</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {result.metadata.sensor_names.map((sensor, index) => (
                  <div key={sensor} className="text-center p-3 bg-muted rounded">
                    <div className="text-xs text-muted-foreground">{sensor}</div>
                    <div className="font-mono text-lg font-bold">{result.input_data[index]}</div>
                  </div>
                ))}
              </div>
              <p className="text-xs text-muted-foreground mt-4">
                Dữ liệu được lấy lúc: {new Date(result.metadata.timestamp).toLocaleString("vi-VN")}
              </p>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}
