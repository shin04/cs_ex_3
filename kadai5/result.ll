define void @prime(){
  @n = common global i32 0, align 4
  @x = common global i32 0, align 4
  %None = common global i32 0, align 4
  %1 = load i32, i32* @x, align 4
  no code
  store i32 %2, i32* %None, align 4
  br label %3
  3:
  %4 = load i32, i32* @x, align 4
  %5 = load i32, i32* @x, align 4
  %6 = load i32, i32* %None, align 4
  no code
  %8 = load i32, i32* %None, align 4
  %9 = mul nsw i32 %7, %8
  %10 = icmp ne i32 %4, %9
  br i1 %10, label %11, label %14
  11:
  %12 = load i32, i32* %None, align 4
  %13 = sub nsw i32 %12, 1
  store i32 %13, i32* %None, align 4
  br label %3
  14:
  %15 = load i32, i32* %None, align 4
  %16 = icmp eq i32 %15, 1
  br i1 %16, label %17, label %19
  17:
  %18 = load i32, i32* @x, align 4
  br label %19
  19:
  br label %20
  20:
  %21 = load i32, i32* @n, align 4
  %22 = icmp slt i32 1, %21
  br i1 %22, label %23, label %27
  23:
  %24 = load i32, i32* @n, align 4
  store i32 %24, i32* @x, align 4
  %25 = load i32, i32* @n, align 4
  %26 = sub nsw i32 %25, 1
  store i32 %26, i32* @n, align 4
  br label %20
  27:
  ret i32 0
}
