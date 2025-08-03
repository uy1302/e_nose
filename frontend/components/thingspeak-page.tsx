"use client"

import { useState, useEffect, useRef, useCallback } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { CardChart } from "@/components/ui/card-chart"
import { Badge } from "@/components/ui/badge"
import { Cloud, Brain, TreePine, Zap, Network, Target, ChevronDown, Play, Pause } from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartData,
  ChartOptions,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);


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

interface PredictionResult {
  class_id?: number
  class_label: string
  probability?: number
}

interface ThingSpeakPrediction {
  input_data?: number[]
  sensor_arrays?: number[][]  // Mảng 10 data points
  predictions: {
    base_1: PredictionResult
    base_2: PredictionResult
    base_3: PredictionResult
    base_4: PredictionResult
    meta: PredictionResult
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
    model_versions?: {
      [key: string]: string
    }
  }
}

interface ChartDataPoint {
  time: string
  value: number
}

interface SensorChartData {
  mq136: ChartDataPoint[]
  mq137: ChartDataPoint[]
  temp: ChartDataPoint[]
  humid: ChartDataPoint[]
}

const odorLabels: { [key: string]: string } = {
  "Thịt loại 1": "Thịt loại 1",
  "Thịt loại 2": "Thịt loại 2", 
  "Thịt loại 3": "Thịt loại 3",
  "Thịt loại 4": "Thịt loại 4",
  "Thịt hỏng": "Thịt hỏng",
}

// Wrapper for charts to handle loading/empty states
const ChartWrapper = ({ children, data, isStreaming }: { children: React.ReactNode, data: any[], isStreaming: boolean }) => {
  if (isStreaming && data.length === 0) {
    return (
        <div className="flex items-center justify-center h-full text-muted-foreground">
            Đang tải dữ liệu...
        </div>
    );
  }

  if (!isStreaming && data.length === 0) {
      return (
          <div className="flex items-center justify-center h-full text-muted-foreground">
              Không có dữ liệu.
          </div>
      );
  }

  return <>{children}</>;
};

const chartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: false,
        },
        tooltip: {
            callbacks: {
                title: (context) => `Time: ${context[0].label}`,
                label: (context) => {
                    const label = context.dataset.label || '';
                    const value = context.parsed.y;
                    return `${label}: ${value.toFixed(2)}`;
                },
            },
        },
    },
    scales: {
        x: {
            ticks: {
                font: {
                    size: 10,
                },
            },
            grid: {
                color: 'rgba(255, 255, 255, 0.1)',
            }
        },
        y: {
            ticks: {
                font: {
                    size: 10,
                },
            },
            grid: {
                color: 'rgba(255, 255, 255, 0.1)',
            }
        },
    },
};

const formatChartJsData = (data: ChartDataPoint[], label: string, color: string): ChartData<'line'> => {
    return {
        labels: data.map(p => p.time),
        datasets: [
            {
                label: label,
                data: data.map(p => p.value),
                borderColor: color,
                backgroundColor: `${color}80`, // Add some transparency to fill color
                pointRadius: 4,
                pointBackgroundColor: color,
                tension: 0.1
            },
        ],
    };
};

export default function ThingSpeakPage() {
  const apiKey = "P91SEPV5ZZG00Y4S"
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<ThingSpeakPrediction | null>(null)
  const [error, setError] = useState<string | null>(null)
  
  // Chart data states
  const [chartData, setChartData] = useState<SensorChartData>({
    mq136: [],
    mq137: [],
    temp: [],
    humid: []
  })
  const [currentDataIndex, setCurrentDataIndex] = useState(0)
  const [pendingSensorArrays, setPendingSensorArrays] = useState<number[][]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const [currentAverageData, setCurrentAverageData] = useState<number[]>([0, 0, 0, 0])
  
  // Auto-refresh states
  const [isAutoRefresh, setIsAutoRefresh] = useState(false)
  const refreshInterval = 30 // seconds - fixed to 30s, not configurable by user
  const streamInterval = 3 // seconds - add data every 3 seconds
  const maxDataPoints = 15 // maximum data points per chart
  const abortControllerRef = useRef<AbortController | null>(null)
  const streamingTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const isRunningRef = useRef(false)
  const pendingSensorArraysRef = useRef<number[][]>([])
  const currentDataIndexRef = useRef(0)

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
      }
      if (streamingTimeoutRef.current) {
        clearTimeout(streamingTimeoutRef.current)
      }
    }
  }, [])

  // Add data to charts with limit
  const addDataToCharts = useCallback((sensorData: number[]) => {
    const timestamp = new Date().toLocaleTimeString("vi-VN")
    
    setChartData(prev => {
      const newData = { ...prev }
      
      // Add new data point for each sensor
      const sensors = ['mq136', 'mq137', 'temp', 'humid'] as const
      sensors.forEach((sensor, index) => {
        const newPoint = {
          time: timestamp,
          value: sensorData[index] || 0
        }
        
        // Add new point and keep only last maxDataPoints
        newData[sensor] = [...prev[sensor], newPoint].slice(-maxDataPoints)
      })
      
      // Calculate new averages from current chart data
      const newAverages = sensors.map((sensor, index) => {
        const sensorData = newData[sensor]
        if (sensorData.length === 0) return 0
        const sum = sensorData.reduce((acc, point) => acc + point.value, 0)
        return sum / sensorData.length
      })
      
      setCurrentAverageData(newAverages)
      
      return newData
    })
  }, [maxDataPoints])

  // Stream data from pending arrays
  const streamNextDataPoint = useCallback(() => {
    const currentIndex = currentDataIndexRef.current
    const arrays = pendingSensorArraysRef.current
    
    if (currentIndex < arrays.length) {
      const dataPoint = arrays[currentIndex]
      addDataToCharts(dataPoint)
      
      const nextIndex = currentIndex + 1
      currentDataIndexRef.current = nextIndex
      setCurrentDataIndex(nextIndex)
      
      // Schedule next data point
      if (nextIndex < arrays.length) {
        streamingTimeoutRef.current = setTimeout(streamNextDataPoint, streamInterval * 1000)
      } else {
        setIsStreaming(false)
        setPendingSensorArrays([])
        pendingSensorArraysRef.current = []
        currentDataIndexRef.current = 0
        setCurrentDataIndex(0)
      }
    }
  }, [addDataToCharts, streamInterval])

  // Sync refs with state
  useEffect(() => {
    pendingSensorArraysRef.current = pendingSensorArrays
  }, [pendingSensorArrays])
  
  useEffect(() => {
    currentDataIndexRef.current = currentDataIndex
  }, [currentDataIndex])

  // Start streaming when new data arrives
  useEffect(() => {
    if (pendingSensorArrays.length > 0 && !isStreaming && currentDataIndex === 0) {
      setIsStreaming(true)
      streamNextDataPoint()
    }
  }, [pendingSensorArrays, isStreaming, currentDataIndex, streamNextDataPoint])

  const handlePredict = useCallback(async () => {
    setIsLoading(true)
    setError(null)

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
      
      // Start streaming if we have sensor arrays
      if (data.sensor_arrays && data.sensor_arrays.length > 0) {
        // Clear any previous streaming
        if (streamingTimeoutRef.current) {
          clearTimeout(streamingTimeoutRef.current)
        }
        
        setPendingSensorArrays(data.sensor_arrays)
        setCurrentDataIndex(0)
        setIsStreaming(false) // Will be set to true by useEffect
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Có lỗi xảy ra khi kết nối ThingSpeak")
      // Stop auto-refresh on error
      setIsAutoRefresh(false)
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Sleep function for delay
  const sleep = (seconds: number): Promise<void> => {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(resolve, seconds * 1000)
      
      // Handle abort
      if (abortControllerRef.current) {
        abortControllerRef.current.signal.addEventListener('abort', () => {
          clearTimeout(timeoutId)
          reject(new Error('Aborted'))
        })
      }
    })
  }

  // Auto-refresh loop with while true pattern
  const startAutoRefreshLoop = useCallback(async () => {
    if (isRunningRef.current) return // Already running
    
    isRunningRef.current = true
    abortControllerRef.current = new AbortController()
    
    try {
      while (isRunningRef.current && !abortControllerRef.current?.signal.aborted) {
        // Fetch data
        await handlePredict()
        
        if (!isRunningRef.current) break
        
        // Wait for next refresh
        await sleep(refreshInterval)
      }
    } catch (err) {
      if (err instanceof Error && err.message !== 'Aborted') {
        console.error('Auto-refresh error:', err)
        setError("Có lỗi xảy ra trong quá trình auto-refresh")
        setIsAutoRefresh(false)
      }
    } finally {
      isRunningRef.current = false
    }
  }, [handlePredict])

  const stopAutoRefresh = useCallback(() => {
    isRunningRef.current = false
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }
    if (streamingTimeoutRef.current) {
      clearTimeout(streamingTimeoutRef.current)
    }
    setIsStreaming(false)
    setCurrentDataIndex(0)
    setPendingSensorArrays([])
  }, [])

  const toggleAutoRefresh = () => {
    if (isAutoRefresh) {
      stopAutoRefresh()
      setIsAutoRefresh(false)
    } else {
      setIsAutoRefresh(true)
    }
  }



  // Auto-refresh effect
  useEffect(() => {
    if (isAutoRefresh) {
      startAutoRefreshLoop()
    } else {
      stopAutoRefresh()
    }
  }, [isAutoRefresh, startAutoRefreshLoop, stopAutoRefresh])



  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Cloud className="mr-2 h-5 w-5" />
            Dự đoán từ ThingSpeak
          </CardTitle>
          <CardDescription>Thu thập dữ liệu từ cảm biến khí, nhiệt độ, độ ẩm và thực hiện dự đoán chất lượng thực phẩm</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Auto-refresh control */}
          <div className="flex justify-center">
            <Button
              variant={isAutoRefresh ? "destructive" : "default"}
              onClick={toggleAutoRefresh}
              disabled={isLoading}
              className="w-full max-w-md"
            >
              {isAutoRefresh ? (
                <>
                  <Pause className="mr-2 h-4 w-4" />
                  Dừng thu thập dữ liệu
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Bắt đầu thu thập dữ liệu
                </>
              )}
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
        <>
          {/* Meta Model Result - Main Result */}
          {result.predictions.meta && (
            <Card className="border-2 border-primary">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="h-5 w-5 mr-2" />
                  Kết quả dự đoán cuối cùng (Mô hình tổng hợp)
                </CardTitle>
                <CardDescription>
                  Kết quả được tối ưu hóa từ 4 mô hình AI cơ sở với dữ liệu ThingSpeak
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center space-y-4">
                  <div className="text-4xl font-bold text-primary">
                    {odorLabels[result.predictions.meta.class_label] || result.predictions.meta.class_label}
                  </div>
                  <div className="text-lg text-muted-foreground">
                    Độ tin cậy: {((result.predictions.meta?.probability || 0) * 100).toFixed(2)}%
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
                  <CardTitle className="text-sm font-medium">Base Model 1</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold">{odorLabels[result.predictions.base_1.class_label] || result.predictions.base_1.class_label}</div>
                  <div className="text-sm text-muted-foreground mt-1">
                    Độ tin cậy: {((result.predictions.base_1.probability || 0) * 100).toFixed(2)}%
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                  <TreePine className="h-4 w-4 mr-2" />
                  <CardTitle className="text-sm font-medium">Base Model 2</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold">{odorLabels[result.predictions.base_2.class_label] || result.predictions.base_2.class_label}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                  <Zap className="h-4 w-4 mr-2" />
                  <CardTitle className="text-sm font-medium">Base Model 3</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold">{odorLabels[result.predictions.base_3.class_label] || result.predictions.base_3.class_label}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center space-y-0 pb-2">
                  <Network className="h-4 w-4 mr-2" />
                  <CardTitle className="text-sm font-medium">Base Model 4</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-xl font-bold">{odorLabels[result.predictions.base_4.class_label] || result.predictions.base_4.class_label}</div>
                </CardContent>
              </Card>
            </div>
          </Collapsible>

          {/* Real-time Sensor Charts */}
          <Card>
            <CardContent>
              {/* Dữ liệu trung bình */}
              <div className="mb-6">
                <h4 className="text-sm font-medium mb-3">Dữ liệu trung bình (cập nhật theo thời gian thực)</h4>
                <div className="grid grid-cols-4 gap-4">
                  {['Amoniac', 'Hydro Sulfide', 'Nhiệt độ', 'Độ ẩm'].map((sensorName, index) => {
                    const unit = sensorName === 'Nhiệt độ' ? '°C' : sensorName === 'Độ ẩm' ? '%' : '';
                    return (
                      <div key={sensorName} className="text-center p-3 bg-primary/10 rounded">
                        <div className="text-xs text-muted-foreground">{sensorName}</div>
                        <div className="font-mono text-lg font-bold">
                          {currentAverageData[index] ? `${currentAverageData[index].toFixed(2)}${unit}` : 'N/A'}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

            </CardContent>
          </Card>

          {/* Charts Card */}
          <Card style={{ backgroundColor: 'rgba(0,0,0,0)', border: 'none', boxShadow: 'none' }}>
            <CardContent>
              {/* Charts Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[500px] w-full">
                {/* Amonia Chart */}
                <CardChart
                  title="Cảm biến Amoniac"
                  description="Đọc dữ liệu cảm biến khí"
                  chartHeight="h-[350px]"
                  dataInfo={`Điểm dữ liệu: ${chartData.mq136.length}/${maxDataPoints}`}
                  className="h-full"
                >
                    <ChartWrapper data={chartData.mq136} isStreaming={isStreaming}>
                        <div className="relative h-full">
                                                       <Line options={chartOptions} data={formatChartJsData(chartData.mq136, 'Amoniac', '#2563eb')} />
                        </div>
                    </ChartWrapper>
                </CardChart>

                {/* Hydro Sulfide Chart */}
                <CardChart
                  title="Cảm biến Hydro Sulfide"
                  description="Đọc dữ liệu cảm biến khí"
                  chartHeight="h-[350px]"
                  dataInfo={`Điểm dữ liệu: ${chartData.mq137.length}/${maxDataPoints}`}
                  className="h-full"
                >
                    <ChartWrapper data={chartData.mq137} isStreaming={isStreaming}>
                        <div className="relative h-full">
                            <Line options={chartOptions} data={formatChartJsData(chartData.mq137, 'Hydro Sulfide', '#dc2626')} />
                        </div>
                    </ChartWrapper>
                </CardChart>

                {/* Temperature Chart */}
                <CardChart
                  title="Nhiệt độ"
                  description="Đọc dữ liệu nhiệt độ (°C)"
                  chartHeight="h-[350px]"
                  dataInfo={`Điểm dữ liệu: ${chartData.temp.length}/${maxDataPoints}`}
                  className="h-full"
                >
                    <ChartWrapper data={chartData.temp} isStreaming={isStreaming}>
                        <div className="relative h-full">
                            <Line options={chartOptions} data={formatChartJsData(chartData.temp, 'Nhiệt độ', '#16a34a')} />
                        </div>
                    </ChartWrapper>
                </CardChart>

                {/* Humidity Chart */}
                <CardChart
                  title="Độ ẩm"
                  description="Đọc dữ liệu độ ẩm (%)"
                  chartHeight="h-[350px]"
                  dataInfo={`Điểm dữ liệu: ${chartData.humid.length}/${maxDataPoints}`}
                  className="h-full"
                >
                    <ChartWrapper data={chartData.humid} isStreaming={isStreaming}>
                        <div className="relative h-full">
                           <Line options={chartOptions} data={formatChartJsData(chartData.humid, 'Độ ẩm', '#ca8a04')} />
                        </div>
                    </ChartWrapper>
                </CardChart>
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  )
}
