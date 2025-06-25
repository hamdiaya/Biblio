'use client'
import BookCard from '@/components/bookCard';
import BookDetailsCard from '@/components/bookDetailsCard';
import axios from 'axios';
import { title } from 'process';


import React, {  use, useEffect, useState } from 'react';

const books:any=[
  {
    key:1,
    title:"all the light we cannot see",
    author:"anthony doerr",
    rating:4.5,
    desc:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Purus morbi eleifend enim, tristique ",
    imgUrl:"/livre.jpg"
  },
  {
    key:2,
    title:"all the light we cannot see",
    author:"anthony doerr",
    rating:4.5,
    desc:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Purus morbi eleifend enim, tristique ",
    imgUrl:"/livre.jpg"
  },
  {
    key:3,
    title:"all the light we cannot see",
    author:"anthony doerr",
    rating:4.5,
    desc:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Purus morbi eleifend enim, tristique ",
    imgUrl:"/livre.jpg"
  },
  {
    key:4,
    title:"all the light we cannot see",
    author:"anthony doerr",
    rating:4.5,
    desc:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Purus morbi eleifend enim, tristique ",
    imgUrl:"/livre.jpg"
  },{
    key:5,
    title:"all the light we cannot see",
    author:"anthony doerr",
    rating:4.5,
    desc:"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Purus morbi eleifend enim, tristique ",
    imgUrl:"/livre.jpg"
  }

];

const  page = ({ params }: { params: Promise<{ book_title: string }> }) => {
  const [books_info, setBooks_info] = useState<any>();

  const[title,setTitle]=useState("");
  const [recommonded_books,setRecommonded_books]=useState([]);
  const [author_books,setauthor_books]=useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const { book_title } = use(params);
  useEffect(() => {
    // Fetch popular books
    const fetchBooks = async () => {
      try {
        const title=(await params).book_title;
        setTitle(decodeURIComponent(title));
        const response = await axios.get(`http://127.0.0.1:8000/getBookInfo/${title}`);
       setBooks_info(response.data.general_info)
       setRecommonded_books(response.data.recommended_books)
       setauthor_books(response.data.author_books)
       console.log(response.data.general_info.desc.length)
        setLoading(false);
      } catch (err) {
        console.log(err)
        setError("Failed to fetch popular books.");
        setLoading(false);
      }
    };

    fetchBooks();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        {/* Loading Spinner */}
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-[#F5B900]"></div>
      </div>
    );
  }
  if (error) return <p>{error}</p>;

  return (
    <div className=''>
      {/* Section with background image */}
     <div className='relative  '>
     <div
        className="w-full h-[550px] bg-cover bg-center  bg-red-600"
        style={{ backgroundImage: "url('/details_bg.jpg')" }}
      >
        {/* Card positioned at the bottom-left */}
        <div className="absolute top-40 left-28 m-4">
          <BookDetailsCard title={title} author={books_info.book_author} rating={books_info.rating} reads={books_info.reads} desc={books_info.desc} imgUrl={(books_info.image_url_y==''?"/not_found.jpg":books_info.image_url_y)} />
        </div>
        
      </div>
     </div>
    {
      (books_info.desc.length>900)?
     <div className="invisible h-[800px]"></div>:
     <div className="invisible h-[390px]"></div>
    }
    
      <div className="bg-white w-full clear-both ">
      <div className=' pt-[73px] px-[170px] '>
     {/* recommonded for you section */}
     <h1 className=' text-[25px] font-semibold pb-8 '>Recommended for You</h1>
    
      {/* book container */}
      <div className=' grid grid-cols-2 gap-[100px] pb-10 '>
          {
            recommonded_books.map((book:any, index:number)=>{
              return <BookCard key={index} title={book.title} author={book.book_authors} rating={book.book_rating} desc={book.book_desc} imgUrl={(book.image_url_y==''?"/not_found.jpg":book.image_url_y)} />
            })
          }
           </div>
     </div>
    {
      (author_books.length!=0)?
      <div className=' pt-[73px] px-[170px] pb-10'>
      {/* recommonded for you section */}
      <h1 className=' text-[25px] font-semibold pb-8 '>Top Reads of {books_info.book_author}</h1>
     
       {/* book container */}
       <div className=' grid grid-cols-2 gap-[100px] '>
           {
             author_books.map((book:any,index:number)=>{
               return <BookCard key={index} title={book.title} author={books_info.book_author} rating={book.book_rating} desc={book.book_desc} imgUrl={(book.image_url_y==''?"/not_found.jpg":book.image_url_y)}/>
             })
           }
            </div>
      </div>:null
    }
      </div>
    </div>
  );
};

export default page;
