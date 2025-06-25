import React from 'react'
import BookCard from './bookCard'

const popular_books = ({books}:{books:any}) => {
  return (
    <div className= 'bg-[#F5F6F8] p-[115px] pb-10 '>
      {/* books container */}
       <div className=' bg-white w-full px-[100px] py-[70px] '>
            <h1 className='text-[40px] font-semibold pb-[60px] '>
            Popular Books
            </h1>
           <div className=' grid grid-cols-2 gap-[100px] '>
          {
            books.map((book:any, index:number)=>{
              return <BookCard key={index} title={book.antecedents} author={book.book_authors} rating={book.book_rating} desc={book.book_desc} imgUrl={(book.image_url_y==''?"/not_found.jpg":book.image_url_y)}/>
            })
          }
           </div>
       </div>
    </div>
  )
}

export default popular_books