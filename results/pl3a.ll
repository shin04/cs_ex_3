@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@i = common global i32 0, align 4
@j = common global i32 0, align 4
@n = common global i32 0, align 4
@a = common global i32 0, align 4
define void @initialize(i32){
}
declare i32 @scanf(i8*, ...)
define void @swap(i32){
  %2 = alloca i32, align 4
  store i32 %0, i32* %2, align 4
  %3 = alloca i32, align 4
  %4 = load i32, i32* %3, align 4
  %5 = load i32, i32* @a, align 4
  store i32 %5, i32* %3, align 4
  %6 = load i32, i32* %3, align 4
  %7 = load i32, i32* %3, align 4
  %8 = add nsw i32 %7, 1
  %9 = load i32, i32* @a, align 4
  store i32 %9, i32* @a, align 4
  %10 = load i32, i32* %3, align 4
  %11 = add nsw i32 %10, 1
  %12 = load i32, i32* %3, align 4
  store i32 %12, i32* @a, align 4
  ret void
}
define i32 @main(){
  %1 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* @n)
  %2 = load i32, i32* @n, align 4
  %3 = icmp sle i32 %2, 100
  br i1 %3, label %4, label undifined
  4:
  %5 = load i32, i32* @n, align 4
  %6 = call i32 @initialize(i32 %5)
  %7 = load i32, i32* @n, align 4
  store i32 %7, i32* @i, align 4
  br label %8
  8:
  %9 = load i32, i32* @i, align 4
  %10 = icmp sle i32 1, %9
  br i1 %10, label %11, label %35
  11:
  store i32 1, i32* @j, align 4
  br label %12
  12:
  %13 = load i32, i32* @j, align 4
  %14 = load i32, i32* @i, align 4
  %15 = icmp slt i32 %13, %14
  br i1 %15, label %16, label %29
  16:
  %17 = load i32, i32* @j, align 4
  %18 = load i32, i32* @a, align 4
  %19 = load i32, i32* @j, align 4
  %20 = add nsw i32 %19, 1
  %21 = load i32, i32* @a, align 4
  %22 = icmp sgt i32 %20, %21
  br i1 %22, label %23, label %36
  23:
  %24 = load i32, i32* @j, align 4
  %25 = call i32 @swap(i32 %24)
  br label %26
  26:
  %27 = load i32, i32* @j, align 4
  %28 = add nsw i32 %27, 1
  store i32 %28, i32* @j, align 4
  br label %12
  29:
  %30 = load i32, i32* @i, align 4
  %31 = load i32, i32* @a, align 4
  %32 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %31)
  %33 = load i32, i32* @i, align 4
  %34 = sub nsw i32 %33, 1
  store i32 %34, i32* @i, align 4
  br label %8
  35:
  br label %36
  36:
  ret i32 0
}
declare i32 @scanf(i8*, ...)
declare i32 @printf(i8*, ...)
