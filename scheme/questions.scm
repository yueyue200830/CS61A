(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.

(define (cons-all first rests)
  (map
    (lambda
      (x)
      (cons first x)
    )
    rests
  )
)

(define (zip pairs)
  (if (null? pairs)
    (cons nil (cons nil nil))
    (begin
      (define next (zip (cdr pairs)))
      (if (null? next)
        (begin
          (define first nil)
          (define second nil)
        )
        (begin
          (define first (car next))
          (define second (car (cdr next)))
        )
      )
      (cons
        (cons (car (car pairs)) first)
        (cons (append (cdr (car pairs)) second) nil)
      )
    )
  )
)

;; Problem 17
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 17
  (begin
    (define (loop n list)
      (if (null? list)
        nil
        (cons (cons n (cons (car list) nil)) (loop (+ n 1) (cdr list)))
      )
    )
    (loop 0 s)
  )
)
  ; END PROBLEM 17

;; Problem 18
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN PROBLEM 18
  (cond
    ((= total 0) (cons nil nil))
    ((or (< total 0) (null? denoms)) nil)
    (else
      (append
        (cons-all
          (car denoms)
          (list-change (- total (car denoms)) denoms)
        )
        (list-change total (cdr denoms))
      )
    )
  )
)
  ; END PROBLEM 18

;; Problem 19
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((quoted? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
        )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
           (cons
             form
             (cons
              params
              (map
                (lambda (x) (let-to-lambda x))
                body
              )
             )
            )
           ; END PROBLEM 19
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
           (begin
            (define result (zip values))
            (append
              (cons
                (cons 'lambda
                  (cons
                    (car result)
                    (map
                      (lambda (x) (let-to-lambda x))
                      body
                    )
                  )
                )
                nil
              )
              (map
                (lambda (x) (let-to-lambda x))
                (cadr result)
              )
            )
           )
           ; END PROBLEM 19
           ))
        (else
         ; BEGIN PROBLEM 19
         (cons
          (car expr)
          (map
            (lambda (x) (let-to-lambda x))
            (cdr expr)
          )
         )
         ; END PROBLEM 19
         )
  )
)
