import * as React from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface CardChartProps {
  title: string
  description?: string
  children: React.ReactNode
  chartHeight?: string
  dataInfo?: string
  className?: string
}

export function CardChart({
  title,
  description,
  children,
  chartHeight = "h-64",
  dataInfo,
  className
}: CardChartProps) {
  return (
    <Card className={cn(className)}>
      <CardHeader className="pb-3">
        <CardTitle className="text-lg">{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        {/* Vùng chứa biểu đồ với chiều cao cố định */}
        <div className={cn("w-full", chartHeight)}>
          {/* FIX: Thêm một div bọc với h-full.
            Điều này rất quan trọng cho các thư viện như Recharts, 
            vì ResponsiveContainer cần một parent có height: 100%.
          */}
          <div className="h-full w-full">
            {children}
          </div>
        </div>
        {dataInfo && (
          <p className="text-xs text-muted-foreground mt-2">
            {dataInfo}
          </p>
        )}
      </CardContent>
    </Card>
  )
}
