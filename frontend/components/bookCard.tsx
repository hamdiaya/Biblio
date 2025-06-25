import Image from 'next/image';
import React from 'react';
import { Rating } from "primereact/rating";
import Link from 'next/link';

const BookCard = ({title,author,rating,desc,imgUrl}:{title:string;author:string;rating:number;desc:string;imgUrl:string;}) => {
  const sanitizedTitle = encodeURIComponent(title);
  return (
   <Link href={`/book/${sanitizedTitle}`}>
    <div className="flex  w-[416px]  h-full ">
      {/* Image Section */}
      <div className="w-full h-full">
        <Image
          src={imgUrl}
          alt="livre"
          width={190}
          height={190}
          className="object-cover  "
        />
      </div>

    
      <div className="w-full   flex flex-col place-content-between ">
        <div>
        <h1 className=" text-2xl pb-5 font-medium line-clamp-2 ">
          {title}
        </h1>
        <h2 className="text-gray-700 text-base pb-3">
          by {author}
        </h2>
        <Rating
          value={rating}
          cancel={false}
          readOnly
          className="text-yellow-500 flex gap-1 pb-6 "
        />
        </div>
        <p className="text-sm text-[#626262] line-clamp-6 ">
         {desc}
        </p>
      </div>
    </div>
   </Link>
  );
};

export default BookCard;
