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

(define (parse s)
  (let* ([xs (regexp-split "\n" s)]
         [xs (dropf xs (negate header))]
         [xs (filter (negate summary?) xs)]
         [xs (gather-by header xs)])
    (write-json xs)))

;; (parse (file->string "example.txt"))

(module+ main
  (parse (port->string (current-input-port))))
