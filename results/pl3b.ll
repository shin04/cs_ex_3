@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@a = common global [100 x i32] zeroinitializer, align 4
@i = common global i32 0, align 4
@n = common global i32 0, align 4
define void @initialize(){
  %1 = alloca i32, align 4
  store i32 2, i32* %1, align 4
  br label %2
  2:
  %3 = load i32, i32* %1, align 4
  %4 = icmp sle i32 %3, 100
  br i1 %4, label %5, label %12
  5:
  %6 = load i32, i32* %1, align 4
  %7 = sext i32 %6 to i64
  %8 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %7
  store i32 0, i32* %8, align 4
  br label %9
  9:
  %10 = load i32, i32* %1, align 4
  %11 = add nsw i32 %10, 1
  store i32 %11, i32* %1, align 4
  br label %2
  12:
  ret void
}
define void @check(i32){
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  %3 = alloca i32, align 4
  %4 = load i32, i32* %2, align 4
  store i32 %4, i32* %3, align 4
  br label %5
  5:
  %6 = load i32, i32* %3, align 4
  %7 = icmp sle i32 %6, 100
  br i1 %7, label %8, label %15
  8:
  %9 = load i32, i32* %3, align 4
  %10 = sext i32 %9 to i64
  %11 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %10
  store i32 1, i32* %11, align 4
  %12 = load i32, i32* %3, align 4
  %13 = load i32, i32* %2, align 4
  %14 = add nsw i32 %12, %13
  store i32 %14, i32* %3, align 4
  br label %5
  15:
  ret void
}
define i32 @main(){
  call void @initialize()
  %1 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* @n)
  %2 = load i32, i32* @n, align 4
  %3 = icmp sle i32 %2, 100
  br i1 %3, label %4, label %24
  4:
  store i32 2, i32* @i, align 4
  %5 = load i32, i32* @n, align 4
  br label %6
  6:
  %7 = load i32, i32* @i, align 4
  %8 = icmp sle i32 %7, %5
  br i1 %8, label %9, label %23
  9:
  %10 = load i32, i32* @i, align 4
  %11 = sext i32 %10 to i64
  %12 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %11
  %13 = load i32, i32* %12, align 4
  %14 = icmp eq i32 %13, 0
  br i1 %14, label %15, label %19
  15:
  %16 = load i32, i32* @i, align 4
  %17 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %16)
  %18 = load i32, i32* @i, align 4
  call void @check(i32 %18)
  br label %19
  19:
  br label %20
  20:
  %21 = load i32, i32* @i, align 4
  %22 = add nsw i32 %21, 1
  store i32 %22, i32* @i, align 4
  br label %6
  23:
  br label %24
  24:
  ret i32 0
}
declare i32 @scanf(i8*, ...)
declare i32 @printf(i8*, ...)
