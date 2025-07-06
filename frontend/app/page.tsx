"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { motion, AnimatePresence } from "framer-motion"
import { useState } from "react"
import PredictionPage from "@/components/prediction-page"
import ThingSpeakPage from "@/components/thingspeak-page"
import SensorsPage from "@/components/sensors-page"
import ModelsPage from "@/components/models-page"

// Animation variants for tab content
const tabVariants = {
  initial: { 
    opacity: 0, 
    x: 20,
    scale: 0.98
  },
  in: { 
    opacity: 1, 
    x: 0,
    scale: 1
  },
  out: { 
    opacity: 0, 
    x: -20,
    scale: 0.98
  }
}

const tabTransition = {
  type: "tween" as const,
  ease: "easeInOut" as const,
  duration: 0.3
}

export default function HomePage() {
  const [activeTab, setActiveTab] = useState("home")

  const handleTabChange = (value: string) => {
    setActiveTab(value)
  }

  return (
    <div className="container mx-auto p-6">
      <motion.div 
        className="mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold tracking-tight">E-Nose Dashboard</h1>
        <p className="text-muted-foreground">Hệ thống dự đoán mùi từ dữ liệu cảm biến</p>
      </motion.div>

      <Tabs value={activeTab} onValueChange={handleTabChange} className="w-full">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.2 }}
        >
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger 
              value="home"
              className="transition-all duration-200 hover:scale-105"
            >
              Trang chủ
            </TabsTrigger>
            <TabsTrigger 
              value="prediction"
              className="transition-all duration-200 hover:scale-105"
            >
              Dự đoán
            </TabsTrigger>
            <TabsTrigger 
              value="thingspeak"
              className="transition-all duration-200 hover:scale-105"
            >
              ThingSpeak
            </TabsTrigger>
            <TabsTrigger 
              value="sensors"
              className="transition-all duration-200 hover:scale-105"
            >
              Cảm biến
            </TabsTrigger>
            <TabsTrigger 
              value="models"
              className="transition-all duration-200 hover:scale-105"
            >
              Mô hình
            </TabsTrigger>
          </TabsList>
        </motion.div>

        <AnimatePresence mode="wait">
          <TabsContent value="home" className="space-y-4">
            {activeTab === "home" && (
              <motion.div
                key="home"
                variants={tabVariants}
                initial="initial"
                animate="in"
                exit="out"
                transition={tabTransition}
                className="space-y-4"
              >
                <motion.div 
                  className="grid gap-4 md:grid-cols-2 lg:grid-cols-4"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.6, delay: 0.3 }}
                >
                  {[
                    { title: "Tổng số cảm biến", value: "8", desc: "6 cảm biến khí + 2 cảm biến môi trường" },
                    { title: "Mô hình AI", value: "3", desc: "ANN, Random Forest, XGBoost" },
                    { title: "Loại mùi", value: "4", desc: "Nước mắm, Tỏi, Chanh, Sữa" },
                    { title: "Độ chính xác", value: "100%", desc: "Trên tập dữ liệu test" }
                  ].map((item, index) => (
                    <motion.div
                      key={item.title}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.4, delay: 0.4 + index * 0.1 }}
                    >
                      <Card className="card-hover-glow">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                          <CardTitle className="text-sm font-medium">{item.title}</CardTitle>
                        </CardHeader>
                        <CardContent>
                          <div className="text-2xl font-bold counter-animate">{item.value}</div>
                          <p className="text-xs text-muted-foreground">{item.desc}</p>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </motion.div>

                <motion.div 
                  className="grid gap-4 md:grid-cols-2"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.8 }}
                >
                  <Card className="card-hover-glow glass-morphism">
                    <CardHeader>
                      <CardTitle>Giới thiệu hệ thống</CardTitle>
                      <CardDescription>E-Nose - Electronic Nose System</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <p className="text-sm">
                        Hệ thống mũi điện tử sử dụng 8 cảm biến để phát hiện và phân loại mùi. Dữ liệu từ các cảm biến được xử
                        lý bởi 3 mô hình AI khác nhau để đưa ra dự đoán chính xác về loại mùi.
                      </p>
                      <div className="space-y-1">
                        <p className="text-sm">
                          <strong>Cảm biến khí:</strong> MQ2, MQ3, MQ4, MQ6, MQ7, MQ135
                        </p>
                        <p className="text-sm">
                          <strong>Cảm biến môi trường:</strong> Nhiệt độ, Độ ẩm
                        </p>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="card-hover-glow glass-morphism">
                    <CardHeader>
                      <CardTitle>Hướng dẫn sử dụng</CardTitle>
                      <CardDescription>Các bước để thực hiện dự đoán</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2">
                      <div className="space-y-2">
                        {[
                          'Chuyển đến tab "Dự đoán"',
                          'Nhập dữ liệu 8 cảm biến',
                          'Nhấn "Dự đoán" để xem kết quả',
                          'Xem kết quả từ 3 mô hình AI'
                        ].map((step, index) => (
                          <motion.div
                            key={step}
                            className="flex items-center space-x-2"
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.3, delay: 1.0 + index * 0.1 }}
                          >
                            <div className="w-6 h-6 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-xs font-bold btn-interactive">
                              {index + 1}
                            </div>
                            <p className="text-sm">{step}</p>
                          </motion.div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              </motion.div>
            )}
          </TabsContent>

          <TabsContent value="prediction">
            {activeTab === "prediction" && (
              <motion.div
                key="prediction"
                variants={tabVariants}
                initial="initial"
                animate="in"
                exit="out"
                transition={tabTransition}
              >
                <PredictionPage />
              </motion.div>
            )}
          </TabsContent>

          <TabsContent value="thingspeak">
            {activeTab === "thingspeak" && (
              <motion.div
                key="thingspeak"
                variants={tabVariants}
                initial="initial"
                animate="in"
                exit="out"
                transition={tabTransition}
              >
                <ThingSpeakPage />
              </motion.div>
            )}
          </TabsContent>

          <TabsContent value="sensors">
            {activeTab === "sensors" && (
              <motion.div
                key="sensors"
                variants={tabVariants}
                initial="initial"
                animate="in"
                exit="out"
                transition={tabTransition}
              >
                <SensorsPage />
              </motion.div>
            )}
          </TabsContent>

          <TabsContent value="models">
            {activeTab === "models" && (
              <motion.div
                key="models"
                variants={tabVariants}
                initial="initial"
                animate="in"
                exit="out"
                transition={tabTransition}
              >
                <ModelsPage />
              </motion.div>
            )}
          </TabsContent>
        </AnimatePresence>
      </Tabs>
    </div>
  )
}
