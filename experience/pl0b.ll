; ModuleID = 'pl0b.c'
source_filename = "pl0b.c"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"

@x = common global i32 0, align 4
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@n = common global i32 0, align 4
; Function Attrs: noinline nounwind optnone ssp uwtable
define void @prime() #0 {
  %1 = alloca i32, align 4
  %2 = load i32, i32* @x, align 4
  %3 = sdiv i32 %2, 2
  store i32 %3, i32* %1, align 4
  br label %4

4:                                                ; preds = %12, %0
  %5 = load i32, i32* @x, align 4
  %6 = load i32, i32* @x, align 4
  %7 = load i32, i32* %1, align 4
  %8 = sdiv i32 %6, %7
  %9 = load i32, i32* %1, align 4
  %10 = mul nsw i32 %8, %9
  %11 = icmp ne i32 %5, %10
  br i1 %11, label %12, label %15

12:                                               ; preds = %4
  %13 = load i32, i32* %1, align 4
  %14 = sub nsw i32 %13, 1
  store i32 %14, i32* %1, align 4
  br label %4

15:                                               ; preds = %4
  %16 = load i32, i32* %1, align 4
  %17 = icmp eq i32 %16, 1
  br i1 %17, label %18, label %21

18:                                               ; preds = %15
  %19 = load i32, i32* @x, align 4
  %20 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %19)
  br label %21

21:                                               ; preds = %18, %15
  ret void
}
declare i32 @printf(i8*, ...) #1
; Function Attrs: noinline nounwind optnone ssp uwtable
define i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* @n)
  br label %3

3:                                                ; preds = %6, %0
  %4 = load i32, i32* @n, align 4
  %5 = icmp slt i32 1, %4
  br i1 %5, label %6, label %10

6:                                                ; preds = %3
  %7 = load i32, i32* @n, align 4
  store i32 %7, i32* @x, align 4
  call void @prime()
  %8 = load i32, i32* @n, align 4
  %9 = sub nsw i32 %8, 1
  store i32 %9, i32* @n, align 4
  br label %3

10:                                               ; preds = %3
  ret i32 0
}
declare i32 @scanf(i8*, ...) #1

attributes #0 = { noinline nounwind optnone ssp uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "darwin-stkchk-strong-link" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "probe-stack"="___chkstk_darwin" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { "correctly-rounded-divide-sqrt-fp-math"="false" "darwin-stkchk-strong-link" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "probe-stack"="___chkstk_darwin" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0, !1, !2}
!llvm.ident = !{!3}

!0 = !{i32 2, !"SDK Version", [2 x i32] [i32 11, i32 1]}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 7, !"PIC Level", i32 2}
!3 = !{!"Apple clang version 12.0.0 (clang-1200.0.32.28)"}
