#lang racket

(require json)

;; If `s` the start of an error item, return a hash of the elements,
;; else return #f.
(define (header s)
  (match s
    [(pregexp "^([^:]+):(\\d+):(\\d+):\\s+(.*)$"
              (list _ file line col desc))
     (hash 'file file 'line line 'col col 'desc desc)]
    [_ #f]))
            
;; Is `s` a summary line such as "3 warnings generated."?
(define (summary? s)
  (match s
    [(pregexp "^\\d+ warnings? generated.") #t]
    [_ #f]))

(define (gather-by f? xs)
  (match xs
    [(cons x xs)
     (define run  (takef xs (negate f?)))
     (define more (dropf xs (negate f?)))
     (define fx (f? x))
     (if fx
         (cons (hash-set fx 'body (string-join run "\n")) (gather-by f? more))
         (list))]
    [(list) (list)]))

;; Offensive phrases, each with a "weight" (how much it contributes to
;; a bad score).
(define offensive-phrases
  (hash "undefined" 1
        "pointer" 10
        "initialize" 1
        "division by zero" 1
        "insecure" 10
        ;; specific risky C stdlib functions:
        "getpw" 10
        "strcpy" 10
        "strcat" 10
        "vfork" 10))

(define (offenses s)
  (for/sum ([(phrase weight) offensive-phrases])
    (* weight (length (regexp-match* phrase s)))))

(define (parse s)
  (let* ([xs (regexp-split "\n" s)]
         [xs (dropf xs (negate header))]
         [xs (filter (negate summary?) xs)]
         [xs (gather-by header xs)]
         [dings (offenses s)]
         [perfect 10]
         [score (- perfect dings (length xs))] ;; can be negative
         [report (hash 'score score
                       'items xs)])
    (write-json report)))

;; (parse (file->string "example.txt"))

(module+ main
  (parse (port->string (current-input-port))))
