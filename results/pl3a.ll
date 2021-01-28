@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@i = common global i32 0, align 4
@j = common global i32 0, align 4
@n = common global i32 0, align 4
@a = common global [100 x i32] zeroinitializer, align 4
define void @initialize(i32){
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  %3 = alloca i32, align 4
  store i32 1, i32* %3, align 4
  %4 = load i32, i32* %2, align 4
  br label %5
  5:
  %6 = load i32, i32* %3, align 4
  %7 = icmp sle i32 %6, %4
  br i1 %7, label %8, label %16
  8:
  %9 = load i32, i32* %3, align 4
  %10 = sext i32 %9 to i64
  %11 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %10
  %12 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %11)
  br label %13
  13:
  %14 = load i32, i32* %3, align 4
  %15 = add nsw i32 %14, 1
  store i32 %15, i32* %3, align 4
  br label %5
  16:
  ret void
}
declare i32 @scanf(i8*, ...)
define void @swap(i32){
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  %3 = alloca i32, align 4
  %4 = load i32, i32* %2, align 4
  %5 = sext i32 %4 to i64
  %6 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %5
  %7 = load i32, i32* %6, align 4
  store i32 %7, i32* %3, align 4
  %8 = load i32, i32* %2, align 4
  %9 = add nsw i32 %8, 1
  %10 = sext i32 %9 to i64
  %11 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %10
  %12 = load i32, i32* %11, align 4
  %13 = load i32, i32* %2, align 4
  %14 = sext i32 %13 to i64
  %15 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %14
  store i32 %12, i32* %15, align 4
  %16 = load i32, i32* %3, align 4
  %17 = load i32, i32* %2, align 4
  %18 = add nsw i32 %17, 1
  %19 = sext i32 %18 to i64
  %20 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %19
  store i32 %16, i32* %20, align 4
  ret void
}
define i32 @main(){
  %1 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* @n)
  %2 = load i32, i32* @n, align 4
  %3 = icmp sle i32 %2, 100
  br i1 %3, label %4, label %40
  4:
  %5 = load i32, i32* @n, align 4
  call void @initialize(i32 %5)
  %6 = load i32, i32* @n, align 4
  store i32 %6, i32* @i, align 4
  br label %7
  7:
  %8 = load i32, i32* @i, align 4
  %9 = icmp sle i32 1, %8
  br i1 %9, label %10, label %39
  10:
  store i32 1, i32* @j, align 4
  br label %11
  11:
  %12 = load i32, i32* @j, align 4
  %13 = load i32, i32* @i, align 4
  %14 = icmp slt i32 %12, %13
  br i1 %14, label %15, label %31
  15:
  %16 = load i32, i32* @j, align 4
  %17 = sext i32 %16 to i64
  %18 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %17
  %19 = load i32, i32* %18, align 4
  %20 = load i32, i32* @j, align 4
  %21 = add nsw i32 %20, 1
  %22 = sext i32 %21 to i64
  %23 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %22
  %24 = load i32, i32* %23, align 4
  %25 = icmp sgt i32 %19, %24
  br i1 %25, label %26, label %28
  26:
  %27 = load i32, i32* @j, align 4
  call void @swap(i32 %27)
  br label %28
  28:
  %29 = load i32, i32* @j, align 4
  %30 = add nsw i32 %29, 1
  store i32 %30, i32* @j, align 4
  br label %11
  31:
  %32 = load i32, i32* @i, align 4
  %33 = sext i32 %32 to i64
  %34 = getelementptr inbounds [100 x i32], [100 x i32]* @a, i64 0, i64 %33
  %35 = load i32, i32* %34, align 4
  %36 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %35)
  %37 = load i32, i32* @i, align 4
  %38 = sub nsw i32 %37, 1
  store i32 %38, i32* @i, align 4
  br label %7
  39:
  br label %40
  40:
  ret i32 0
}
declare i32 @printf(i8*, ...)
