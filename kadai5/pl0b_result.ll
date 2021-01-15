@n = common global i32 0, align 4
@x = common global i32 0, align 4
define void @prime(){
  %1 = alloca i32, align 4
  %2 = load i32, i32* @x, align 4
  %3 = sdiv nsw i32 %2, 2
  store i32 %3, i32* %1, align 4
  br label %4
  4:
  %5 = load i32, i32* @x, align 4
  %6 = load i32, i32* @x, align 4
  %7 = load i32, i32* %1, align 4
  %8 = sdiv nsw i32 %6, %7
  %9 = load i32, i32* %1, align 4
  %10 = mul nsw i32 %8, %9
  %11 = icmp ne i32 %5, %10
  br i1 %11, label %12, label %15
  12:
  %13 = load i32, i32* %1, align 4
  %14 = sub nsw i32 %13, 1
  store i32 %14, i32* %1, align 4
  br label %4
  15:
  %16 = load i32, i32* %1, align 4
  %17 = icmp eq i32 %16, 1
  br i1 %17, label %18, label %20
  18:
  %19 = load i32, i32* @x, align 4
  br label %20
  20:
  ret void
}
define i32 @main(){
  br label %1
  1:
  %2 = load i32, i32* @n, align 4
  %3 = icmp slt i32 1, %2
  br i1 %3, label %4, label %8
  4:
  %5 = load i32, i32* @n, align 4
  store i32 %5, i32* @x, align 4
  call void @prime()
  %6 = load i32, i32* @n, align 4
  %7 = sub nsw i32 %6, 1
  store i32 %7, i32* @n, align 4
  br label %1
  8:
  ret i32 0
}
